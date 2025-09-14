# TODO List - Resume Site

## Security & Maintenance

### Convert Static JS/CSS to CDN-based Dependencies

**Priority: Medium**

Convert locally hosted JavaScript and CSS libraries to CDN-based versions for easier security updates and better performance.

**Current static files to convert:**
- `assets/plugins/jquery-3.7.1.min.js` → jQuery CDN
- `assets/plugins/bootstrap/js/bootstrap.min.js` → Bootstrap CDN  
- `assets/plugins/bootstrap/css/bootstrap.min.css` → Bootstrap CDN
- `assets/plugins/font-awesome/css/all.css` → Font Awesome CDN

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