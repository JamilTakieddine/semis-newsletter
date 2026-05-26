<<<<<<< HEAD
# Semiconductor Daily Briefing — Newsletter Agent

A scheduled agent that searches the web for semiconductor industry news daily,
summarizes it with Claude, and delivers a formatted HTML email to your inbox.

## Architecture

```
Cloud Scheduler (cron: 0 7 * * *)
        ↓
Cloud Run Job (runs ~30s, exits)
        ↓
Claude API (claude-sonnet-4 + web_search tool)
        ↓
Gmail SMTP → your inbox
```

## Local Setup

### 1. Clone and install

```bash
git clone <your-repo>
cd semis-newsletter
pip install -r requirements.txt
```

### 2. Create your .env file

```bash
cp .env.example .env
# Fill in your values
```

**Getting a Gmail App Password:**
1. Go to myaccount.google.com → Security
2. Enable 2-Step Verification (required)
3. Search "App passwords" → create one → name it "semis-newsletter"
4. Copy the 16-character password into `GMAIL_APP_PASSWORD`

**Getting an Anthropic API Key:**
1. Go to console.anthropic.com
2. API Keys → Create Key
3. **Important:** Also go to Settings → Enable web search for your organization

### 3. Run locally

```bash
export $(cat .env | xargs)
python main.py
```

---

## GCP Cloud Run Deployment

### Prerequisites
- `gcloud` CLI installed and authenticated
- A GCP project with billing enabled (free tier covers this workload)

### Step 1: Enable required GCP services

```bash
gcloud services enable \
  run.googleapis.com \
  cloudscheduler.googleapis.com \
  secretmanager.googleapis.com \
  artifactregistry.googleapis.com
```

### Step 2: Store secrets in Secret Manager

```bash
# Store each secret (never put secrets in env vars directly in GCP console)
echo -n "sk-ant-..." | gcloud secrets create ANTHROPIC_API_KEY --data-file=-
echo -n "sender@gmail.com" | gcloud secrets create GMAIL_SENDER --data-file=-
echo -n "xxxx-xxxx-xxxx-xxxx" | gcloud secrets create GMAIL_APP_PASSWORD --data-file=-
echo -n "you@gmail.com" | gcloud secrets create RECIPIENT_EMAIL --data-file=-
```

### Step 3: Build and push Docker image

```bash
export PROJECT_ID=$(gcloud config get-value project)
export REGION=us-central1
export IMAGE=gcr.io/$PROJECT_ID/semis-newsletter

gcloud builds submit --tag $IMAGE
```

### Step 4: Create the Cloud Run Job

```bash
gcloud run jobs create semis-newsletter \
  --image $IMAGE \
  --region $REGION \
  --set-secrets="ANTHROPIC_API_KEY=ANTHROPIC_API_KEY:latest,\
GMAIL_SENDER=GMAIL_SENDER:latest,\
GMAIL_APP_PASSWORD=GMAIL_APP_PASSWORD:latest,\
RECIPIENT_EMAIL=RECIPIENT_EMAIL:latest" \
  --max-retries 1 \
  --task-timeout 120s
```

### Step 5: Schedule it with Cloud Scheduler

```bash
# Runs every day at 7:00 AM Eastern (12:00 UTC)
gcloud scheduler jobs create http semis-newsletter-daily \
  --location $REGION \
  --schedule "0 12 * * *" \
  --uri "https://${REGION}-run.googleapis.com/apis/run.googleapis.com/v1/namespaces/${PROJECT_ID}/jobs/semis-newsletter:run" \
  --http-method POST \
  --oauth-service-account-email $(gcloud iam service-accounts list --format='value(email)' --filter='displayName:Compute Engine default service account')
```

### Step 6: Test it manually

```bash
gcloud run jobs execute semis-newsletter --region $REGION
```

Check the logs:
```bash
gcloud run jobs executions list --job semis-newsletter --region $REGION
```

---

## Cost Estimate

| Resource | Usage | Cost |
|---|---|---|
| Cloud Run Job | ~30s, 512MB RAM, once/day | Free tier |
| Cloud Scheduler | 1 job | Free tier (3 jobs free) |
| Secret Manager | 4 secrets | Free tier |
| Claude Sonnet 4 + web search | ~4K input + 2K output tokens + 8 searches | ~$0.02/day |

**Total: ~$0.50–$0.60/month** (essentially just the API usage)

---

## Customization

- **Change the schedule:** Edit the cron in Cloud Scheduler (`0 12 * * *` = 7AM ET daily)
- **Add more recipients:** Modify `emailer.py` to accept a list and loop `sendmail`
- **Add a Telegram fallback:** Add `python-telegram-bot` and a second delivery function
- **Tune coverage:** Edit the `USER_PROMPT` in `newsletter.py` to add/remove topics
=======
# semis-newsletter
Description: (optional) Semiconductor Daily Briefing Newsletter Agent
>>>>>>> 40286dfe08978468b51635528305ba4c2bf3159f
