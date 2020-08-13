# Introduction to GitHub Actions
## Actions vs. Workflows
Actions are **individual tasks** and workflows are **custom automated processes**

* Workflows: automated processes that run on your repository; workflows can have many GitHub Actions

* GitHub Actions: individual tasks; they can be written using Docker, JavaScript and now also shell scrips with the new Composite Run Steps; you can write your own actions or use an action someone else created

## Writing your first workflow
Workflows are defined using `YAML` files and you must store them in the `.github/workflows` directory of your repository
To create a workflow we need to define these things:
* **The event** that triggers the workflow
* **The machine** each job should run
* **The jobs** that make the workflow (jobs contain a set of steps that perform individual tasks and run in parallel by default)
* **The steps** each job should run

```yaml
# your-repo-name/.github/workflows/first_workflow.yml
name: First Workflow                                               
on: push                                                  
jobs:                         
  first-job:                           
    name: Say hi                           
    runs-on: ubuntu-latest                           
    steps:                           
    - name: Print a greeting                             
      run: echo Hi from our first workflow!
```

## Using an Action in your workflow
Actions are individual tasks and we can use them from three sources:
* Actions defined in the same repository as the workflow
* Actions defined in a public repository
* Actions defined in an published Docker container image

Let's use an Action that prints ASCII art text:

```yaml
# your-repo-name/.github/workflows/first_workflow.yml
name: First Workflow
on: push                                                  
jobs:                         
  first-job:                           
    name: Say hi                           
    runs-on: ubuntu-latest                           
    steps:                           
      - name: Print a greeting                             
        run: echo Hi from our first workflow!   
     
      - name: Show ASCII greeting                             
        uses: mscoutermarsh/ascii-art-action@master   
        with:                               
          text: 'HELLO!'
```

## Using Python with workflows
Setting a specific version of Python or PyPy is the recommended way of using Python with GitHub Actions. To do that we'll use an action: `setup-python`. In this example we'll run a Python script defined in the same repository as the workflow. To do that we also need to use the `checkout` action to access the file.

```yaml
# your-repo-name/.github/workflows/first_workflow.yml
name: First Workflow
on: push                                                  
jobs:                         
  get-posts-job:                            
    name: Get TDS posts                            
    runs-on: ubuntu-latest     
    steps:                             
      - name: Check-out the repo under $GITHUB_WORKSPACE                               
        uses: actions/checkout@v2         
                                                  
      - name: Set up Python 3.8                               
        uses: actions/setup-python@v2                               
        with:                                 
          python-version: '3.8'          
                                                  
      - name: Install Scrapy                               
        run: pip install scrapy         
 
      - name: Get TDS posts about GitHub Actions                                 
        run: scrapy runspider posts_spider.py -o posts.json
```

## Persisting workflow data
An artifact is a file or collection of files produced during a workflow run. We can pass an artifact to another job in the same workflow or download it using the GitHub UI. To work with artifacts we use the `upload-artifact` and `download-artifact` actions.

```yaml
# your-repo-name/.github/workflows/first_workflow.yml
name: First Workflow
on: push                                                  
jobs:                         
  get-posts-job:                            
    name: Get TDS posts                            
    runs-on: ubuntu-latest     
    steps:                             
      - name: Check-out the repo under $GITHUB_WORKSPACE                               
        uses: actions/checkout@v2         
                                                  
      - name: Set up Python 3.8                               
        uses: actions/setup-python@v2                               
        with:                                 
          python-version: '3.8'          
                                                  
      - name: Install Scrapy                               
        run: pip install scrapy         
 
      - name: Get TDS posts about GitHub Actions                                 
        run: scrapy runspider posts_spider.py -o posts.json
        
      - name: Upload artifact                      
        uses: actions/upload-artifact@v2                        
        with:                                 
          name: posts                                 
          path: posts.json
```
You can download the file using the GitHub UI.

## Creating your first Action
Actions can be created using Docker containers, JavaScript or you can create an action using shell scripts (a composite run steps action). The main use case for the composite run steps action is when you have a lot of shell scripts to automate tasks and writing a shell script to combine them is easier than JavaScript or Docker.

The filename for an action must be either `action.yml` or `action.yaml`. Let's use the example from GitHub Docs and create an action that prints a "Hey [user]" message. Since it's a composite action we'll use the `using: "composite"` syntax:

```yaml
# action.yml
name: 'Hey From a GitHub Action'
description: 'Greet someone'
inputs:
  user:  # id of input
    description: 'Who to greet'
    required: true
    default: 'You'
runs:
  using: "composite"
  steps: 
    - run: echo Hey ${{ inputs.user }}.
      shell: bash
```

If an  action is defined in the same repository as the workflow we can refer to it using `./path-to-action-file`. In this case we need to access the file inside the repository, so  we also need to use the `checkout` action.

### Running an action from the same repository

```yaml
# .github/workflows/use-action-same-repo.yml
name: Action from the same repo
on: push 
jobs:                                 
  use-your-own-action:                           
    name: Say Hi using your own action                           
    runs-on: ubuntu-latest                           
    steps:                             
      - uses: actions/checkout@v2
                                                            
      - uses: ./ # the action.yml file is in the root folder                              
        with:                                
         user: 'Déborah'
```

### Running an action from a public repository
```yaml
# .github/workflows/use-action-public-repo.yml
name: Action from a public repository
on: push 
jobs:                                 
  use-your-own-action:                           
    name: Say Hi using your own action                           
    runs-on: ubuntu-latest                           
    steps:                                               
      - uses: dmesquita/github-actions-tutorial@master                            
        with:                                
         user: 'Déborah'
```


