# NY-23 Accountability Tracker - Project Status

## ✅ Completed Setup

### Site Infrastructure
- ✅ Hugo static site generator installed
- ✅ Clean, professional Ananke theme configured
- ✅ GitHub Actions workflow for automatic deployment
- ✅ Content structure created (fact-checks, votes, methodology, correspondence)
- ✅ Site builds successfully

### Core Pages Created
- ✅ Homepage with tagline "Documenting NY-23 representation through public records"
- ✅ Methodology page (establishes credibility and standards)
- ✅ Fact-check template with verification checklist
- ✅ Example entry showing format

### Repository Setup
- ✅ Git repository initialized
- ✅ .gitignore configured
- ✅ README for developers
- ✅ SETUP guide for anonymous deployment

## 📋 Next Steps (In Order)

### 1. Anonymous GitHub Setup (30 minutes)
- [ ] Create ProtonMail account
- [ ] Create anonymous GitHub account
- [ ] Create public repository
- [ ] Push initial commit
- [ ] Enable GitHub Pages in repo settings

### 2. Manual Collection Phase (2-4 weeks)
- [ ] Collect 10-15 strongest examples of contradictions
- [ ] Document verification process for each
- [ ] Create fact-check entries using template
- [ ] Perfect methodology
- [ ] Get trusted reviewers to check accuracy

### 3. Domain Purchase (Optional - $12)
- [ ] Buy domain with privacy protection
- [ ] Configure DNS to point to GitHub Pages
- [ ] Update baseURL in hugo.toml
- [ ] Enable HTTPS enforcement

### 4. Soft Launch (Week 5)
- [ ] Publish first 10 entries
- [ ] Share anonymously on r/Buffalo
- [ ] Post in WNY political groups
- [ ] Send to local journalists as resource
- [ ] Monitor response

### 5. Automation (Later - if sustainable)
- [ ] Build Python scraper for press releases
- [ ] Add voting record cross-reference
- [ ] Set up keyword flagging system
- [ ] Create submission form for constituents

## 📁 Project Structure

```
langworthy-tracker/
├── .github/workflows/hugo.yml    # Auto-deploy to GitHub Pages
├── content/
│   ├── _index.md                 # Homepage
│   ├── fact-checks/              # Statement vs. action entries
│   │   └── example-entry.md      # Template showing format
│   ├── votes/                    # Voting record documentation
│   ├── methodology/              # Verification standards
│   │   └── _index.md            # Core credibility page
│   └── correspondence/           # Constituent letter examples
├── archetypes/
│   └── fact-checks.md           # Template for new entries
├── themes/ananke/               # Professional Hugo theme
├── hugo.toml                     # Site configuration
├── README.md                     # Developer documentation
├── SETUP.md                      # Anonymous deployment guide
└── PROJECT_STATUS.md            # This file

```

## 🎯 Success Criteria

### Phase 1: Credibility (Weeks 1-4)
- 10-15 bulletproof fact-check entries published
- Zero factual errors
- All sources verified and archived
- Methodology page establishes standards
- Trusted reviewers approve accuracy

### Phase 2: Traction (Weeks 5-8)
- Site shared in local communities
- Local journalists aware of resource
- Constituents submitting tips
- No successful challenges to accuracy

### Phase 3: Impact (Month 3+)
- Regular weekly updates
- Growing readership
- Media citations
- Accountability conversations in district

## 💰 Total Cost

**Current**: $0
**With domain**: $12/year
**Optional upgrades**: $0-10/month for enhanced hosting (not needed initially)

## 🔒 Anonymity Safeguards

- Separate GitHub account with ProtonMail
- Domain with privacy protection
- No identifying information in content
- Version-controlled for transparency
- Can claim ownership later when appropriate

## 📝 Content Standards

Every entry must have:
1. Exact quote with date
2. Primary source link (congress.gov, official sites)
3. Archive.org archived URL
4. Screenshot saved locally
5. Full context provided
6. No opinion or speculation

## 🚀 Quick Start Commands

```bash
# Navigate to project
cd /Users/zachbeaudoin/Langworthywatch/langworthy-tracker

# Create new fact-check entry
hugo new content/fact-checks/YYYY-MM-DD-topic.md

# Test locally
hugo server -D
# Then visit http://localhost:1313

# Publish changes
git add .
git commit -m "Add new fact-check entry"
git push  # Auto-deploys via GitHub Actions
```

## ⚠️ Important Reminders

1. **Start manually**: Don't build automation until you've proven the concept
2. **Quality over quantity**: 1-2 solid entries per week beats rushed daily posts
3. **Accuracy is everything**: One error undermines entire project
4. **Stay factual**: No analysis, just documented facts side-by-side
5. **Keep it separate**: Never mention on personal/business accounts

## 🎓 Your Advantages

- Policy research training (CSU/Columbia MA)
- CPACC certification shows attention to standards
- Veteran status (credibility on veterans issues)
- Actual NY-23 constituent
- No campaign affiliation

## 📊 Metrics to Track (Optional)

- Number of entries published
- Page views (via GitHub Pages insights or Plausible)
- Social shares
- Media mentions
- Constituent submissions

## 🔄 Maintenance Schedule

**Weekly** (2-3 hours):
- Monday: Check sources for new material
- Wednesday: Research and verify
- Friday: Write entry, publish

**Monthly**:
- Review all archive links still working
- Check for any errors to correct
- Update if new information emerges

---

**Status**: Ready for anonymous GitHub deployment and manual collection phase.

**Next Action**: Follow SETUP.md to create anonymous GitHub account and push initial commit.
