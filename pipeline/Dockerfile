# to build this image: docker build -t test:pandas .
#-t means "tag"
# the . at the end is the folder where docker looks to find files.

# Start with slim Python 3.13 image
FROM python:3.13.10-slim

# Copy uv binary from official uv image (multi-stage build pattern)
# where is the image: ghcr.io/astral-sh (github containe registry)
# which image: uv:latest
# what to copy: uv (it's a file, not a folder)
# file destination: /bin/ (it's a folder, it ends in /)
COPY --from=ghcr.io/astral-sh/uv:latest /uv /bin/

# Set working directory
# next time COPY is used with a relative path, it will be relative to /app
# also, when RUN is used, it will run from /app
WORKDIR /app

# Add virtual environment to PATH so we can use installed packages
# the variable PATH already has a list of path, separated by a colon.  
# This line adds the path /app/.venv/bin at the beginning of the path list
# The path does not exist yet, but it will be filled later.  
ENV PATH="/app/.venv/bin:$PATH"

# Copy dependency files first (better layer caching)
# copy destination relative to workdir (/app)
COPY "pyproject.toml" "uv.lock" ".python-version" ./ 

# Install dependencies from lock file (ensures reproducible builds)
# uv is found because by default, because /bin is on the default PATH in Debian slim images.  It can be run from any directory.
# however, when uv is run, it looks for uv.lock and pyproject.toml in the working directory -> /app
# running the sync file will install all the packages required to build the environment in the .venv on the host machine.  
RUN uv sync --locked

# Copy application code
# from the host machine (/workspaces/docker-workshop/pipeline/)
# to image/app/
COPY pipeline.py pipeline.py

# Set entry point
# the cli arguments will overwrite this.  
# to reproduce the same behavior, the --entrypoint only takes one argument.  
# for multiple arguments, put the first one after entrypoint, then for further arguments, put them after the image name:
# docker run --entrypoint python myimage pipeline.py 12
ENTRYPOINT ["python", "pipeline.py"]