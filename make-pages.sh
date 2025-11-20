#!/usr/bin/env bash
set -euo pipefail

# Use current folder as base
BASE_DIR="."

files=(
  "foundations/index.md"
  "foundations/welcome.md"
  "foundations/how-to-use-this-wiki.md"
  "foundations/what-is-disability.md"
  "foundations/disability-models.md"
  "foundations/language-terminology-identity.md"
  "foundations/disability-culture.md"
  "foundations/for-allies.md"

  "crisis/index.md"
  "crisis/global-crisis-hotlines.md"
  "crisis/disabled-crisis-support.md"
  "crisis/abuse-neglect-exploitation.md"
  "crisis/emergency-disaster-preparedness.md"

  "community/index.md"
  "community/online-communities.md"
  "community/disability-specific-peer-groups.md"
  "community/in-person-community.md"
  "community/youth-student-communities.md"

  "rights/index.md"
  "rights/global-overview.md"
  "rights/history-of-disability-rights.md"
  "rights/us-federal-rights.md"
  "rights/us-state-rights.md"
  "rights/international-rights.md"
  "rights/advocacy-and-self-advocacy.md"
  "rights/us/ada.md"
  "rights/us/section-504.md"
  "rights/us/idea.md"
  "rights/us/fair-housing-act.md"
  "rights/us/air-carrier-access-act.md"
  "rights/us/state-disability-rights-laws.md"

  "healthcare/index.md"
  "healthcare/accessible-healthcare.md"
  "healthcare/healthcare-rights.md"
  "healthcare/insurance-navigation.md"
  "healthcare/medical-equipment-and-at.md"
  "healthcare/mental-health.md"
  "healthcare/pain-and-fatigue.md"
  "healthcare/home-and-community-care.md"

  "benefits/index.md"
  "benefits/us-benefits-overview.md"
  "benefits/us-ssdi.md"
  "benefits/us-ssi.md"
  "benefits/us-medicaid.md"
  "benefits/us-medicare.md"
  "benefits/us-able-accounts.md"
  "benefits/us-snap.md"
  "benefits/us-tanf.md"
  "benefits/us-state-benefits.md"
  "benefits/us-veterans-benefits.md"
  "benefits/us-family-caregiver-pay.md"
  "benefits/international-benefits-overview.md"
  "benefits/canada-benefits.md"
  "benefits/uk-benefits.md"
  "benefits/australia-benefits.md"
  "benefits/eu-benefits.md"
  "benefits/other-countries-benefits.md"
  "benefits/debt-budgeting-financial-rights.md"
  "benefits/benefit-denials-and-appeals.md"

  "housing/index.md"
  "housing/accessible-housing-search-guide.md"
  "housing/housing-rights.md"
  "housing/home-modifications.md"
  "housing/tenants-rights-with-disabilities.md"
  "housing/homelessness-and-disability.md"
  "housing/group-homes-and-institutions.md"
  "housing/independent-living-philosophy-and-centers.md"

  "education/index.md"
  "education/early-intervention.md"
  "education/k12-education.md"
  "education/higher-education.md"
  "education/adult-and-continuing-education.md"
  "education/transition-to-adulthood.md"

  "employment/index.md"
  "employment/job-searching-with-a-disability.md"
  "employment/workplace-accommodations.md"
  "employment/employment-rights-by-country.md"
  "employment/supported-employment-and-voc-rehab.md"
  "employment/entrepreneurship-and-self-employment.md"

  "transport/index.md"
  "transport/public-transit-rights.md"
  "transport/paratransit.md"
  "transport/air-travel-rights.md"
  "transport/driving-and-adaptive-driving.md"
  "transport/mobility-aids.md"
  "transport/service-animals.md"

  "relationships/index.md"
  "relationships/dating-and-relationships.md"
  "relationships/sexuality-and-reproductive-health.md"
  "relationships/parenting-with-a-disability.md"
  "relationships/parents-of-disabled-children.md"
  "relationships/caregiving.md"
  "relationships/abuse-safety-and-consent.md"

  "daily-living/index.md"
  "daily-living/assistive-technology-overview.md"
  "daily-living/personal-care.md"
  "daily-living/cooking-and-nutrition.md"
  "daily-living/exercise-and-adaptive-sports.md"
  "daily-living/recreation-travel-and-outdoors.md"
  "daily-living/accessible-travel.md"
  "daily-living/fashion-beauty-and-adaptive-wear.md"
  "daily-living/pets-and-service-animals.md"

  "tech/index.md"
  "tech/web-accessibility.md"
  "tech/mobile-and-os-accessibility.md"
  "tech/communication-access-and-aac.md"
  "tech/gaming-accessibility.md"
  "tech/social-media-accessibility.md"
  "tech/digital-disability-justice.md"

  "conditions/index.md"
  "conditions/physical-disabilities.md"
  "conditions/sensory-disabilities.md"
  "conditions/chronic-illness.md"
  "conditions/neurodivergence.md"
  "conditions/intellectual-and-developmental-disability.md"
  "conditions/psychiatric-and-psychosocial-disability.md"
  "conditions/invisible-disabilities.md"
  "conditions/multiple-disabilities.md"
  "conditions/rare-diseases.md"

  "intersectionality/index.md"
  "intersectionality/race-and-disability.md"
  "intersectionality/gender-and-disability.md"
  "intersectionality/lgbtq-and-disability.md"
  "intersectionality/religion-and-disability.md"
  "intersectionality/immigration-and-refugees.md"
  "intersectionality/poverty-and-class.md"
  "intersectionality/incarceration-and-criminalization.md"
  "intersectionality/rural-disability.md"
  "intersectionality/indigenous-disability-perspectives.md"
  "intersectionality/disability-and-homelessness.md"

  "media/index.md"
  "media/books.md"
  "media/blogs-and-websites.md"
  "media/podcasts.md"
  "media/youtube-channels.md"
  "media/tiktok-creators.md"
  "media/documentaries-and-films.md"
  "media/tv-shows.md"
  "media/disability-arts-and-performance.md"
  "media/media-tropes-and-representation.md"
  "media/disabled-creators-directory.md"

  "research/index.md"
  "research/disability-statistics.md"
  "research/academic-programs.md"
  "research/studies-archive.md"
  "research/accessible-research-tools.md"
  "research/ethical-research-with-disabled-communities.md"
  "research/how-to-interpret-disability-data.md"

  "get-involved/index.md"
  "get-involved/advocacy-101.md"
  "get-involved/policy-advocacy.md"
  "get-involved/accessible-protest-guide.md"
  "get-involved/volunteering.md"
  "get-involved/starting-organizations.md"
  "get-involved/community-organizing.md"

  "professionals/index.md"
  "professionals/educators.md"
  "professionals/healthcare-providers.md"
  "professionals/employers-and-hr.md"
  "professionals/social-workers.md"
  "professionals/architects-and-designers.md"
  "professionals/public-safety-officers.md"
  "professionals/emergency-planners.md"

  "glossary/index.md"
  "glossary/terminology.md"
  "glossary/acronyms.md"
  "glossary/bibliography.md"
  "glossary/citation-guide.md"
  "glossary/how-to-contribute.md"
  "glossary/editorial-guidelines.md"

  "regions/index.md"
)

for relpath in "${files[@]}"; do
  filepath="${BASE_DIR}/${relpath}"
  dirpath="$(dirname "$filepath")"
  mkdir -p "$dirpath"

  if [[ -f "$filepath" ]]; then
    echo "Skipping existing file: $filepath"
    continue
  fi

  title=$(basename "${relpath%.md}" | tr '-' ' ' | sed 's/\b./\u&/g')

  cat > "$filepath" <<EOF
---
title: ${title}
---

# ${title}

_Stub page. This topic will be expanded with community contributions._
EOF

  echo "Created: $filepath"
done

echo "Done."