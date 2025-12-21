# NY-23 Accountability Tracker

Documentation site for NY-23 Congressional representation using public records.

## Built With

- [Hugo](https://gohugo.io/) - Static site generator
- [Ananke Theme](https://github.com/theNewDynamic/gohugo-theme-ananke)

## Local Development

```bash
# Install Hugo (macOS)
brew install hugo

# Run development server
hugo server -D

# Build for production
hugo
```

## Deployment

This site is deployed via GitHub Pages. Push to main branch to deploy.

## Content Structure

- `content/fact-checks/` - Statement vs. action comparisons
- `content/votes/` - Voting record documentation
- `content/methodology/` - Verification standards and process

## Standards

All entries must include:
- Primary source links
- Archive.org archived URLs
- Full context and exact quotes
- No speculation or opinion presented as fact

See `/content/methodology/` for complete standards.
