# TODO LIST

Here is a todo list for my resume website.

## MUST DO

- [ ] Fix credentialurl be used in Certification as a link ... currently unused?
- [ ] Add ETAAC link for 2009 report to Congress - https://www.irs.gov/pub/irs-prior/p3415--2009.pdf
- [ ] Add SOC 2 Compliance work from Envestnet to work section
- [ ] Add Credly certification profile https://www.credly.com/users/michael-mcgarrah
- [x] Add credly SAS cert entries to Resume
- [ ] Use Indeed Profile as PDF short form resume https://profile.indeed.com/p/jm-pfv4s18 ???
- [ ] Add all the LinkedIn projects to Resume as new section
- [ ] https://www.youtube.com/@MichaelMcGarrah/playlists for below projects
  - [ ] AI for Robotics https://www.youtube.com/watch?v=KFo8ECjZyg8&list=PLG_DpV4CFj63n9GYGOhZV1fKbdO_CHNoa
  - [ ] Computation Photography https://www.youtube.com/watch?v=WZPtuNnaqVc&list=PLG_DpV4CFj60wdkJuM2cWBC-uyKEhbYNL
  - [ ] Phonetic Transcriptions https://www.youtube.com/watch?v=WsvWZScw7Tk&list=PLG_DpV4CFj61_ltukKYaYQNipEFOLMqBe
  - [ ] Pull from the custom resume to Accompany Health that I wrote with 4 projects and summaries
- [ ] Update the PDF version of resume to match web print version
- [ ] Write a single entry for 1990-2005 with a summary of work titles and skills... to shorten up the resume. Point to long resume.
- [ ] Add the PDF version from [Google Docs Resume](https://docs.google.com/document/d/1YuYyPKpCZNMarkZHMHJ7_-Tm3dAJ_BvS9kl7iwIFDYQ/edit?usp=sharing)
  - [ ] In data.yaml under section "#pdf: http://www.africau.edu/images/default/sample.pdf"
  - [ ] https://stackoverflow.com/questions/55380596/create-a-pdf-out-of-a-complete-jekyll-page-with-toc
  - [ ] https://github.com/abemedia/jekyll-pdf
  - [ ] Add Jekyll-PDF plugin as project below...
- [ ] Fix the print version to be linear without sidebar - crazy looking when printed out
- [ ] Use the "ChatGPT optimizations" section below list to customize resume for AI/ML version in https://www.mcgarrah.org/aiml-resume/
- [ ] Fix light-gray job headers
    Fix the CSS or SASS for the job headers being a light gray... they wash out badly
- [ ] Add a HR between each job or other method to delinate between the jobs... or make the sub-sections in job details smaller.
- [x] Use Indeed.com resume reviewer to clean up grammar and spelling
- [ ] ATS (Applicant Tracking Systems) score and data fields review
- [ ] Major hiring websites review for terms:
  - LinkedIn Jobs
  - Indeed
  - Glassdoor
  - GovernmentJobs (https://www.governmentjobs.com/careers/northcarolina)
  - Welcome to the Jungle (was a disappointment)
  - Dice.com
  - Monster
  - ZipRecruiter
  - Seek
  - SimplyHired
  - Career Builder
  - Zoho
  - Hired
- [ ] Review StackOverFlow for technical terms on resume and for their skills listings
- [ ] Review Microsoft Profile for Skills list in https://jobs.careers.microsoft.com/global/en/profile (microsoft login)
- [x] Copy work details
    Copy details from [resume-2018-11-05-14-08.pdf](https://drive.google.com/file/d/1JOQZZ6Q81OQlPaJMbojlgaRHit4gfQDV/view?usp=sharing)

## WANT TO DO

- [ ] My personal [Kaggle Homepage](https://www.kaggle.com/mcgarrah) is anemic and needs some of my older work added
- [ ] Create a plain text resume from Jekyll https://www.indeed.com/career-advice/resumes-cover-letters/text-resume
- [ ] Update this to include an image for the university under the date \<div\> section
- [ ] https://www.linkedin.com/pulse/using-chatgpt-write-cover-notes-thomas-redstone-zvghf/
- [ ] https://www.linkedin.com/pulse/making-good-resume-great-chatgpt-eugene-medynskiy-rt79c/
- [ ] https://www.linkedin.com/posts/heyronir_12-chatgpt-prompts-for-a-resume-that-gets-activity-7188427259416928256-ml38/
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

## How to create PDFs for Resume or Posts

    https://github.com/abemedia/jekyll-pdf

    To export a Jekyll site as a PDF file, you can use a dedicated Jekyll plugin like "jekyll-pdf" which leverages a headless browser like wkhtmltopdf to generate PDF versions of your pages by adding a configuration to your Jekyll site, specifying which pages should be converted to PDF and customizing options like page size and layout within your front matter; essentially creating a web version of your site that is then converted to PDF. 

    Key steps:
        Install the plugin:
            Add gem "jekyll-pdf" to your Gemfile.
            Run `bundle install`.
        Configure in _config.yml:
            Add `jekyll-pdf` to your gems list in `_config.yml`.
        Mark pages for PDF generation:
            In the front matter of the pages you want to export as PDF, add `pdf: true`.
        Customize (optional):
            Define a specific PDF layout using a layout file with a `_pdf` suffix (e.g., `post_pdf` for the `post` layout).
            Adjust PDF settings like page size, margins, and headers/footers through front matter options. 
        Example usage:
            Front matter for a page to be converted to PDF:
                Code
                ```yaml
                ---
                layout: default
                pdf: true
                ---
                ```

        Accessing generated PDF link:
            Within your page's HTML, use the liquid variable {{ page.pdf_url }} to access the URL of the generated PDF. 
        Important considerations:
            CSS styling:
            Ensure your CSS is optimized for printing to get the best results in the PDF.
        Complex layouts:
            For more intricate layouts with multiple sections, you might need to adjust the PDF generation process or use additional styling techniques.

--

## ChatGPT optimizations

https://www.linkedin.com/posts/meganlieu_sponsored-genai-activity-7213929270962778112-wQyE?utm_source=share&utm_medium=member_android

𝗽𝗿𝗼𝗺𝗽𝘁𝘀 𝘁𝗼 𝗼𝗽𝘁𝗶𝗺𝗶𝘇𝗲 𝘆𝗼𝘂𝗿 𝗿𝗲𝘀𝘂𝗺𝗲 𝘄𝗶𝘁𝗵 𝗔𝗜:

1️⃣ Give me a list of skills and keywords I should include in my resume if I am targeting [target role]

2️⃣ Write me a professional summary that summarizes the experiences in the attached resume. Include metrics, my total years of experience and make it 2-3 sentences long [paste in resume]

3️⃣ Rewrite my experiences to be impact-driven by following this format: “Accomplished X as measured by Y by doing Z” [paste in experience bullets]

4️⃣ Tailor my resume to the following job description [paste job description]. Here’s my resume [paste in resume]

5️⃣ Please proofread my resume for all spelling and grammatical errors [paste in resume]

Use these prompts on You.com, which is a much more customizable ChatGPT!

It comes with 4 different assistants depending on the task, but it’s the new Custom Assistant feature that makes You.com feel like it was made for, well…YOU.

Try You for free to optimize your resume with AI the smart way today

--
