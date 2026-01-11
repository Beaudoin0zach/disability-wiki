# Setup Guide for Anonymous GitHub Deployment

## Step 1: Create Anonymous GitHub Account

1. Use ProtonMail to create a new email account (e.g., ny23accountability@protonmail.com)
2. Create new GitHub account using that email
3. Choose a generic username (e.g., ny23-tracker, langworthy-watch, etc.)
4. Use Tor Browser or VPN when creating and managing the account

## Step 2: Create GitHub Repository

1. Log into your anonymous GitHub account
2. Create new repository named: `ny23-accountability` or similar
3. Make it **public** (transparency is key)
4. DO NOT initialize with README (we already have one)

## Step 3: Connect Local Repository to GitHub

From your **personal computer** (where you build content):

```bash
cd /Users/zachbeaudoin/Langworthywatch/langworthy-tracker

# Add the remote (replace with your actual GitHub username/repo)
git remote add origin https://github.com/YOUR-ANON-USERNAME/ny23-accountability.git

# Create initial commit
git add .
git commit -m "Initial site setup"

# Push to GitHub
git branch -M main
git push -u origin main
```

## Step 4: Enable GitHub Pages

1. Go to repository Settings → Pages
2. Source: "GitHub Actions"
3. The workflow file (.github/workflows/hugo.yml) will automatically deploy

Your site will be available at: `https://YOUR-ANON-USERNAME.github.io/ny23-accountability/`

## Step 5: Configure Custom Domain (Optional - $12/year)

### Buy Domain Anonymously:
1. Use Namecheap or Porkbun
2. Enable WhoisGuard/privacy protection
3. Pay with privacy.com virtual card
4. Good domain options:
   - LangworthyWatch.org
   - NY23Accountability.org
   - NY23Watch.org

### Point Domain to GitHub Pages:
1. In domain registrar DNS settings, add these records:
   ```
   A @ 185.199.108.153
   A @ 185.199.109.153
   A @ 185.199.110.153
   A @ 185.199.111.153
   CNAME www YOUR-ANON-USERNAME.github.io
   ```

2. In GitHub repo Settings → Pages → Custom domain:
   - Enter your domain (e.g., langworthywatch.org)
   - Check "Enforce HTTPS"

3. Update `hugo.toml`:
   ```toml
   baseURL = 'https://langworthywatch.org/'
   ```

## Step 6: Daily Workflow

### Adding New Fact-Check Entries:

1. Create new file in `content/fact-checks/`:
   ```bash
   hugo new content/fact-checks/2024-12-healthcare-claim.md
   ```

2. Edit the file with your verified content

3. When ready to publish, change `draft: true` to `draft: false`

4. Commit and push:
   ```bash
   git add content/fact-checks/2024-12-healthcare-claim.md
   git commit -m "Add healthcare funding fact-check"
   git push
   ```

5. GitHub Actions will automatically build and deploy (takes ~2 minutes)

### Testing Locally Before Publishing:

```bash
# Start development server
hugo server -D

# Open browser to http://localhost:1313
# Review your changes
# Stop server with Ctrl+C
```

## Anonymity Checklist

- [ ] Using ProtonMail for GitHub account
- [ ] GitHub username not linked to your identity
- [ ] Domain registered with privacy protection
- [ ] Never mention this project on personal social media
- [ ] Don't commit from personal GitHub account
- [ ] No identifying information in content
- [ ] Use VPN/Tor when managing anonymous GitHub (optional but recommended)

## Security Best Practices

1. **Keep work separate**: Don't link this project to Beau Access Solutions
2. **Verify facts rigorously**: You can't afford errors
3. **Archive everything**: Use Archive.org for all source URLs
4. **Version control shows transparency**: All edits are tracked in Git
5. **Never skip the methodology**: Always link sources

## Content Guidelines

### DO:
- ✅ Use exact quotes with dates
- ✅ Link to congress.gov for all votes
- ✅ Archive all sources
- ✅ Present facts without interpretation
- ✅ Include full context

### DON'T:
- ❌ Include your opinion
- ❌ Use inflammatory language
- ❌ Speculate about motives
- ❌ Publish unverified claims
- ❌ Include local knowledge only you would know

## Claiming Ownership Later

If you decide to publicly attach your name later:

1. Add "About" page revealing yourself
2. Update methodology with your credentials
3. Explain why you started anonymously
4. Stand behind every entry

## Cost Summary

- **Free Option**: GitHub Pages + GitHub domain ($0)
- **Professional Option**: Custom domain ($12/year)
- **Optional**: Email newsletter via Mailchimp free tier ($0)

## Next Steps

1. Set up anonymous GitHub account
2. Push initial commit
3. Enable GitHub Pages
4. Collect your first 5-10 strongest examples manually
5. Perfect your verification process
6. Launch when you have solid foundation

---

**Remember**: The best protection is rigorous accuracy. Make every entry bulletproof.
