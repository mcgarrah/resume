# TODO List - Resume Site

## Security & Maintenance

### Convert Static JS/CSS to CDN-based Dependencies

**Priority: Medium**

Convert locally hosted JavaScript and CSS libraries to CDN-based versions for easier security updates and better performance.

**Completed CDN conversions:**
- ✅ `assets/plugins/jquery-3.7.1.min.js` → jQuery CDN (3.7.1)
- ✅ `assets/plugins/bootstrap/js/bootstrap.min.js` → Bootstrap CDN (3.4.1)
- ✅ `assets/plugins/bootstrap/css/bootstrap.min.css` → Bootstrap CDN (3.4.1)
- ✅ `assets/plugins/font-awesome/css/all.css` → Font Awesome CDN (6.6.0)

**Additional components found and converted:**
- Font Awesome upgraded from 5.1.1 to 6.6.0
- All dependencies now use SRI integrity hashes
- Created package.json for Dependabot monitoring
- Updated .gitignore to exclude static dependencies

**Benefits:**
- Automatic security updates via CDN version pinning
- Reduced repository size
- Better caching and performance
- Easier dependency management

**Implementation:**
1. Update `_includes/head.html` and `_includes/scripts.html`
2. Use integrity hashes for security (SRI)
3. Add fallback to local files if CDN fails
4. Remove static library files from repository
5. Update `.gitignore` to exclude future static dependencies

**Example CDN implementation:**
```html
<script src="https://code.jquery.com/jquery-3.7.1.min.js" 
        integrity="sha256-..." 
        crossorigin="anonymous"></script>
```

**Testing required:**
- Verify all interactive components work with CDN versions
- Test offline fallback functionality
- Validate SRI hashes match CDN files