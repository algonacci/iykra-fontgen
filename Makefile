project? = $(shell gcloud config get project)
region ?= $(shell gcloud config get compute/region)
commit_hash ?= $(shell git rev-parse --short HEAD)
ar_host := $(region)-docker.pkg.dev
ar_endpoint := $(ar_host)/$(project)
ar_repo_name := deploy-iykra-fontgen
ar_image_name := $(ar_repo_name)/$(ar_repo_name)
docker_image_name := $(ar_image_name):$(commit_hash) 
ar_image_uri := $(ar_endpoint)/$(docker_image_name)

format:
	ruff format

push:
	@gcloud artifacts repositories create $(ar_repo_name) \
		--location=$(region)
		--repository-format docker || true 2>&1
	@gcloud auth configure-docker $(ar_host)
	@docker built . -t $(docker_image_name) --platform linux/amd64
	@docker tag $(docker_image_name) $(ar_image_uri)
	@docker push $(ar_image_uri)

plan:
	@cd infra/; terraform init
	@cd infra/; terraform plan \
		-var image_uri=$(ar_image_uri) \
		-var PROJECT_ID=$(project) \
		-var GCP_REGION=$(region)

deploy:
	@cd infra/; terraform init
	@cd infra/; terraform apply \
		-var image_uri=$(ar_image_uri) \
		-var PROJECT_ID=$(project) \
		-var GCP_REGION=$(region) \
		-auto-approve

destroy:
	@cd infra/; terraform init
	@cd infra/; terraform destroy \
		-var image_uri=$(ar_image_uri) \
		-var PROJECT_ID=$(project) \
		-var GCP_REGION=$(region) \
		-auto-approve