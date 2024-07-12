# TODO LIST

Here is a todo list for my resume website.

## MUST DO

- [ ] Fix the print version to be linear without sidebar - crazy looking when printed out
- [ ] Add the PDF version from [Google Docs Resume](https://docs.google.com/document/d/1YuYyPKpCZNMarkZHMHJ7_-Tm3dAJ_BvS9kl7iwIFDYQ/edit?usp=sharing)
- [ ] Fix light-gray job headers
    Fix the CSS or SASS for the job headers being a light gray... they wash out badly
- [ ] Add a HR between each job or other method to delinate between the jobs... or make the sub-sections in job details smaller.
- [x] Use Indeed.com resume reviewer to clean up grammar and spelling
- [ ] ATS (Applicant Tracking Systems) score and data fields review
- [ ] Major hiring websites review for terms:
  - LinkedIn
  - Indeed
  - ZipRecruiter
  - Seek
  - SimplyHired
  - Career Builder 
- [x] Copy work details
    Copy details from https://drive.google.com/file/d/1JOQZZ6Q81OQlPaJMbojlgaRHit4gfQDV/view?usp=sharing (resume-2018-11-05-14-08.pdf)

## WANT TO DO

- [ ] Update this to include an image for the university under the date \<div\> section
- [x] Update to include GPA in the template as well
    /home/mcgarrah/Github/resume/_includes/education.html
- [ ] Certification section with an image
    /home/mcgarrah/Github/resume/_includes/certifications.html
- [ ] Get images of companies and universities 
    /home/mcgarrah/github/resume/assets/images/company-logos/
- [x] Local Jekyll run from VSCode
    https://stackoverflow.com/questions/31561632/run-bundle-exec-command-tasks-in-visual-studio-code

    https://www.google.com/search?q=vscode+bundle+ruby+jekyll&sca_esv=4c52f5fd3cefc50d&sxsrf=ACQVn08l5P6xFbbmShG99-GQ3tFmjFs5Jw%3A1710431237286&ei=BRzzZbiJEZShiLMPtK6LWA&ved=0ahUKEwj4n77yjPSEAxWUEGIAHTTXAgsQ4dUDCBA&uact=5&oq=vscode+bundle+ruby+jekyll&gs_lp=Egxnd3Mtd2l6LXNlcnAiGXZzY29kZSBidW5kbGUgcnVieSBqZWt5bGwyBRAhGKABMgUQIRigATIFECEYnwVI5DdQvQ1Ymi9wAXgBkAEAmAGNAaABzQeqAQM1LjS4AQPIAQD4AQGYAgqgAugHwgIKEAAYRxjWBBiwA8ICBBAjGCfCAgYQABgWGB7CAgsQABiABBiKBRiGA5gDAIgGAZAGCJIHAzYuNKAHpB8&sclient=gws-wiz-serp

    Here's how to run Jekyll from inside Visual Studio Code (VS Code) without extra extensions:
    1. Create a folder and file called tasks.json in the .vscode directory
    2. Create a script called tasks that runs Jekyll serve
    3. The contents of the tasks.json file might look like this: version': '2.0.0' `tasks': ( label': 'Start Jekyll' type': 'shell' command': 'bundle exec jekyll serve --host localhost --port 4000'

OR use the VSCode Plugin...
