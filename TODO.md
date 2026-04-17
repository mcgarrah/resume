# Resume Project Status & TODO

## Current Status
- **Branch**: `feature/jekyll-pandoc-exports`
- **Status**: Clean working tree, up to date with origin
- **Recent Progress**: Successfully integrated jekyll-pandoc-exports plugin for automated DOCX/PDF generation

## Recent Accomplishments ✅
- [x] Integrated jekyll-pandoc-exports plugin for automated document exports
- [x] Fixed credentialurl usage in Certifications with credentialname field
- [x] Added Credly SAS and AWS certification entries
- [x] Reviewed Jekyll and Ruby GitHub Actions upgrades
- [x] Added LinkedIn projects to Resume
- [x] Updated GPA in education template
- [x] Fixed light-gray job headers (hacked CSS)
- [x] Used Indeed.com resume reviewer for grammar/spelling
- [x] Copied work details from legacy resume

## High Priority TODO Items 🔥

### CSS & Layout Issues
- [ ] **Fix wrap section 60px margin** - Remove excessive padding around whole site in CSS _base.scss above line 177
- [ ] **Fix major section vertical margins** - Reduce 60px vertical margin in CSS _base.scss line 177
- [ ] **Improve job header styling** - Fix CSS properly (currently hacked) and add HR between jobs for better delineation
- [ ] **Fix print version** - Make linear layout without sidebar for better printing

### Content Updates
- [ ] **Add ETAAC link** - Include 2009 Congressional report link: https://www.irs.gov/pub/irs-prior/p3415--2009.pdf
- [ ] **Add SOC 2 Compliance work** - Include Envestnet SOC 2 compliance experience in work section
- [ ] **Consolidate 1990-2005 work** - Write single entry summarizing early career to shorten resume

### PDF & Export Features
- [ ] **Update PDF version** - Sync PDF with current web print version
- [ ] **Test jekyll-pandoc-exports** - Verify DOCX/PDF generation is working properly
- [ ] **Configure PDF styling** - Optimize CSS for PDF export format

### Technical Improvements
- [ ] **ATS optimization** - Review for Applicant Tracking Systems compatibility
- [ ] **Create AI/ML specialized version** - Use ChatGPT optimizations for https://www.mcgarrah.org/aiml-resume/

## Medium Priority TODO Items 📋

### Content Enhancements
- [ ] Add coming projects:
  - [ ] Github - URL Redirector (TF HCL)
  - [ ] Github - ADP-AI Automated Document Processing with AI (TF HCL)
- [ ] Create plain text resume version for Indeed
- [ ] Add company/university images to assets/images/company-logos/

### Website Features
- [ ] Add certification section with images
- [ ] Update to include university images under date sections
- [ ] Create Jekyll-PDF plugin project entry

### Job Market Research
- [ ] Review major hiring websites for keyword optimization:
  - LinkedIn Jobs, Indeed, Glassdoor, GovernmentJobs
  - Dice.com, Monster, ZipRecruiter, etc.
- [ ] Review StackOverflow for technical terms
- [ ] Review Microsoft Profile skills list

## Low Priority TODO Items 📝

### Personal Branding
- [ ] Update Kaggle Homepage with older work
- [ ] Add Credly certification profile integration
- [ ] Create cover letter templates using ChatGPT prompts

### Documentation & Process
- [ ] Document local Jekyll VSCode setup
- [ ] Create comprehensive installation guide
- [ ] Add performance monitoring for site builds

## ChatGPT Resume Optimization Prompts 🤖

Use these prompts to optimize resume with AI:

1. **Skills & Keywords**: "Give me a list of skills and keywords I should include in my resume if I am targeting [target role]"

2. **Professional Summary**: "Write me a professional summary that summarizes the experiences in the attached resume. Include metrics, my total years of experience and make it 2-3 sentences long [paste in resume]"

3. **Impact-Driven Experiences**: "Rewrite my experiences to be impact-driven by following this format: 'Accomplished X as measured by Y by doing Z' [paste in experience bullets]"

4. **Job Tailoring**: "Tailor my resume to the following job description [paste job description]. Here's my resume [paste in resume]"

5. **Proofreading**: "Please proofread my resume for all spelling and grammatical errors [paste in resume]"

## Technical Context

### Jekyll-Pandoc-Exports Integration
- **Plugin Status**: Successfully configured in `_config.yml`
- **Features Available**: 
  - Automatic DOCX/PDF generation
  - Unicode cleanup for LaTeX compatibility
  - Download link injection
  - Custom CSS for print styling
- **Configuration**: 0.75in margins, title cleanup patterns configured

### Current Infrastructure
- **Hosting**: GitHub Pages with custom domain
- **Build**: GitHub Actions with Jekyll
- **Analytics**: Google Analytics (G-F90DVB199P)
- **Theme**: Custom ceramic theme with responsive design

## Next Steps Recommendation

1. **Immediate (This Week)**:
   - Fix CSS margin issues for better visual presentation
   - Test PDF/DOCX export functionality
   - Add SOC 2 compliance work to Envestnet section

2. **Short Term (Next 2 Weeks)**:
   - Consolidate early career entries
   - Optimize for ATS systems
   - Create AI/ML specialized version

3. **Long Term (Next Month)**:
   - Complete job market keyword research
   - Implement all remaining content updates
   - Set up automated testing for exports

---
*Last Updated: 2025-01-03*
*Current Branch: feature/jekyll-pandoc-exports*