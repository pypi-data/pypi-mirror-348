# Trelis OpenAI Logger

> **Note:** Currently only supports OpenAI-style APIs. Does not support other LLM providers like Google's Gemini or Anthropic. Although Gemini does support OpenAI style endpoints.

A simple and efficient logging system for LLM interactions using PostgreSQL. Automatically logs all OpenAI API calls including prompts, responses, token usage, and latency.

## Quick Start

1. Install the package:
```bash
uv pip install trelis-openai-logger
```

2. Use in your code:
```python
# Preferred: Import OpenAI directly from trelis_openai_logger
from trelis_openai_logger import OpenAI

# Initialize with database connection and optional OpenAI config
client = OpenAI(
    # Database connection (required)
    pg_dsn="postgresql://localhost/llm_logs",
    # OpenAI configuration (optional)
    # api_key="your-api-key",  # defaults to OPENAI_API_KEY env var
    # base_url="https://api.openai.com/v1",  # useful for OpenAI-compatible APIs
)

# Use normally - all calls are automatically logged
response = client.chat.completions.create(
    model="gpt-4.1-mini",
    messages=[{"role": "user", "content": "What's one and one?"}],
)
```

## Database Setup

Before using the logger, you need a PostgreSQL database. Choose one of these setup options:

### Environment Variables

Create a `.env` file in the project root:

```bash
# Create .env file
cat > .env << EOF
# Required for OpenAI API
OPENAI_API_KEY=your_openai_api_key

# Required for PostgreSQL
DB_PASSWORD=your_secure_password
EOF
```

### Option 1: Local PostgreSQL

```bash
# Install PostgreSQL
brew install postgresql@15
brew services start postgresql@15

# Create database
createdb llm_logs

chmod +x setup/local_setup.sh
./setup/local_setup.sh

# Test connection
uv run test_local_db.py
```

### Option 2: DigitalOcean Droplet (~$12/month)

>![Warning]
>This will incur charges on your DigitalOcean account.

Droplet Specifications:
- 2GB RAM
- 1 vCPU
- 50GB SSD
- Ubuntu 22.04

This configuration is optimized for PostgreSQL performance with:
- Sufficient memory for query caching
- Adequate disk space for log storage
- Cost-effective for development and small production loads

First, complete these prerequisites:

1. Install DigitalOcean CLI:
```bash
# Install CLI
brew install doctl

# Authenticate (you'll need an API token from Digital Ocean dashboard)
doctl auth init
```

2. Set up SSH key:
```bash
# Generate SSH key without password (if you don't have one)
ssh-keygen -t ed25519 -f ~/.ssh/do_llm_logger -N ""

# Add SSH key to Digital Ocean
doctl compute ssh-key import llm-logger --public-key-file ~/.ssh/do_llm_logger.pub
```

Then choose either automated or manual setup:

#### A. Automated Setup (Recommended)

```bash
# Run setup script
chmod +x setup/create_droplet.sh
./setup/create_droplet.sh
```

The script will:
1. Create SSH key if needed
2. Set up the droplet with PostgreSQL
3. Configure remote access
4. Test the connection
5. Provide you with the connection string

#### B. Manual Setup

1. Get the SSH key ID:
```bash
SSH_KEY_ID=$(doctl compute ssh-key list --format ID --no-header)
```

3. Create droplet with PostgreSQL:
```bash
# Create cloud-init config
cat > cloud-init.yml << 'EOF'
#cloud-config
package_update: true
packages: [postgresql, postgresql-contrib]

runcmd:
  - systemctl start postgresql
  - sudo -u postgres createdb llm_logs
  - sudo -u postgres psql -c "ALTER USER postgres PASSWORD '${DB_PASSWORD}';"
  - sudo -u postgres psql -c "ALTER SYSTEM SET listen_addresses TO '*';"
  - echo "host all all 0.0.0.0/0 md5" >> /etc/postgresql/14/main/pg_hba.conf
  - systemctl restart postgresql
EOF

# Create droplet
doctl compute droplet create \
    --image ubuntu-22-04-x64 \
    --size s-1vcpu-1gb \
    --region lon1 \
    --ssh-keys $SSH_KEY_ID \
    --user-data-file cloud-init.yml \
    llm-logger

# Get droplet IP
DROPLET_IP=$(doctl compute droplet list --format PublicIPv4 --no-header)

# Add to known hosts
ssh-keyscan -H $DROPLET_IP >> ~/.ssh/known_hosts

# Wait for setup to complete (~2 minutes)
sleep 120

# Copy and run migrations
scp setup/migrations/01_create_tables.sql root@${DROPLET_IP}:/tmp/
ssh root@${DROPLET_IP} 'sudo -u postgres psql -d llm_logs -f /tmp/01_create_tables.sql'

# Test connection and get your connection string
CONNECTION_STRING="postgresql://postgres:${DB_PASSWORD}@${DROPLET_IP}/llm_logs"

# Add to .env file
echo "DATABASE_URL='${CONNECTION_STRING}'" >> .env

# Now you can run the example
source .env
uv run example.py
```

#### Cleanup

When you're done with the droplet, you can clean up resources:

```bash
# Using the cleanup script (recommended)
./setup/cleanup_droplet.sh

# Or manually
doctl compute droplet list  # Find your droplet ID
doctl compute droplet delete <droplet-id>

# Optionally delete the SSH key from Digital Ocean
doctl compute ssh-key list  # Find your key ID
doctl compute ssh-key delete <key-id>

# Optionally delete the local SSH key
rm ~/.ssh/do_llm_logger ~/.ssh/do_llm_logger.pub
```

### Option 3: DigitalOcean Managed Database (~$17/month)

For production use with automatic backups and scaling. The base price is $15/month plus storage costs ($0.215/GiB/month, 10 GiB minimum):

1. First, create a managed database in DigitalOcean:
```bash
# Create a db-s-1vcpu-2gb cluster in London (2GB RAM recommended for better performance)
doctl databases create llm-logger-db \
    --engine pg \
    --region lon1 \
    --size db-s-1vcpu-2gb \
    --version 14

# The command will output the database ID, save it for the next step
# Example output: ID: 0c164d6a-4185-4e19-ad0e-06301c711f17

# Get the connection details using the database ID
doctl databases connection <database-id>

2. Add the connection URL to your .env file:
```bash
# The connection URL from the previous command (use double quotes, no spaces around =)
DATABASE_URL="postgresql://doadmin:password@host:port/defaultdb?sslmode=require"
```

3. Run the managed database setup script to run migrations:
```bash
source .env
chmod +x setup/managed_db_setup.sh
./setup/managed_db_setup.sh
```

This will:
- Install dbmate if not present
- Run migrations using dbmate on the database

4. Test the connection:
```bash
source .env
uv run example.py
```

To clean up the managed database:
```bash
# Using the database ID from earlier
doctl databases list

doctl databases delete <database-id>
```

## Logging Traces

The `example.py` script can be used to test any of the database configurations. It will:
1. Test the database connection
2. Create a test table
3. Insert and query test data
4. Make a test OpenAI API call with logging

Use it with any of the database options:

```bash
# Local PostgreSQL
DATABASE_URL='postgresql://localhost/llm_logs' uv run example.py

# DigitalOcean Droplet (assuming you have set DATABASE_URL in .env)
source .env
uv run example.py

# DigitalOcean Managed Database (assuming you have set DATABASE_URL in .env)
source .env
uv run example.py
```

The script will show detailed progress with checkmarks (✓) for successful steps or crosses (✗) for failures.

Or you can test manually:

```python
from llm_logger import OpenAI

# Local PostgreSQL
client = OpenAI(
    api_key="your-api-key",
    pg_dsn="postgresql://localhost/llm_logs"
)

# Digital Ocean PostgreSQL
client = OpenAI(
    api_key="your-api-key",
    pg_dsn="postgresql://user:pass@host:port/database"
)

# Use as normal OpenAI client
response = client.chat.completions.create(
    model="gpt-4.1-mini",
    messages=[{"role": "user", "content": "Hello!"}]
)
```

## Querying the Logs

Connect to your PostgreSQL database based on your setup:

```bash
# Local PostgreSQL
psql llm_logs

# DigitalOcean Droplet
# Using environment variables from .env
source .env
PGPASSWORD="$DB_PASSWORD" psql -h your_droplet_ip -U postgres llm_logs

e.g.
source .env
PGPASSWORD="$DB_PASSWORD" psql -h 159.65.58.176 -U postgres llm_logs

# DigitalOcean Managed Database
psql "your_connection_string"

# Or use the connection string from your .env file
source .env
psql "$DATABASE_URL"
```

Useful queries for analyzing your logs:

```sql
-- View recent chat conversations
SELECT 
    to_char(t.created_at, 'YYYY-MM-DD HH24:MI:SS') as time,
    t.model,
    '👤 User' as role,
    p.value->>'content' as message
FROM llm_traces t,
    jsonb_array_elements(t.prompt) p
UNION ALL
SELECT 
    to_char(created_at, 'YYYY-MM-DD HH24:MI:SS') as time,
    model,
    '🤖 Assistant' as role,
    response->'choices'->0->'message'->>'content' as message
FROM llm_traces
ORDER BY time DESC, role DESC
LIMIT 20;

-- Get average latency and token usage by model
SELECT 
    model, 
    COUNT(*) as requests,
    ROUND(AVG(latency_ms)::numeric, 2) as avg_latency_ms,
    ROUND(AVG(total_tokens)::numeric, 2) as avg_tokens
FROM llm_traces 
WHERE error IS NULL
GROUP BY model;

-- Find failed requests in the last 24 hours
SELECT 
    to_char(created_at, 'YYYY-MM-DD HH24:MI:SS') as time,
    model,
    error->>'message' as error_message,
    error->>'type' as error_type
FROM llm_traces
WHERE 
    error IS NOT NULL AND
    created_at > NOW() - INTERVAL '24 hours'
ORDER BY created_at DESC;

-- Get token usage per day
SELECT 
    DATE(created_at) as date,
    model,
    COUNT(*) as requests,
    SUM(prompt_tokens) as prompt_tokens,
    SUM(completion_tokens) as completion_tokens,
    SUM(total_tokens) as total_tokens
FROM llm_traces
WHERE error IS NULL
GROUP BY DATE(created_at), model
ORDER BY date DESC, model;

-- Find similar prompts
SELECT 
    to_char(created_at, 'YYYY-MM-DD HH24:MI:SS') as time,
    model,
    p.value->>'content' as prompt,
    response->'choices'->0->'message'->>'content' as response
FROM llm_traces t,
    jsonb_array_elements(t.prompt) p
WHERE 
    p.value->>'content' ILIKE '%your search term%'
ORDER BY created_at DESC
LIMIT 10;
```

You can also create a `.psqlrc` file in your home directory to improve the psql experience:

```bash
# Create or edit ~/.psqlrc
cat > ~/.psqlrc << 'EOF'
\set PROMPT1 '%[%033[1m%]%M %n@%/%R%[%033[0m%]%# '
\x auto
\set VERBOSITY verbose
\set HISTFILE ~/.psql_history- :DBNAME
\set HISTCONTROL ignoredups
\set COMP_KEYWORD_CASE upper
EOF
```

## Database Schema

The system logs the following information for each interaction:
- Unique trace ID
- Timestamp
- Model used
- Endpoint called
- Full prompt/messages
- Complete response
- Latency
- Token usage
- Any errors that occurred
- Custom metadata

## Publishing to PyPI

1. Update version in `pyproject.toml` if needed
2. Build the package:
```bash
uv build
```
3. Check the built package in `dist/` directory
4. Upload to PyPI under the Trelis organization:
```bash
# Set your PyPI token as an environment variable
export UV_PUBLISH_TOKEN=<your-trelis-pypi-token>

# Publish to PyPI
uv publish --publish-url https://upload.pypi.org/legacy/ --token "${UV_PUBLISH_TOKEN}"
```

Make sure you have:
- Updated all documentation
- Run tests successfully
- Have the Trelis organization PyPI token