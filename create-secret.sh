#

export PROJECT_ID=$(gcloud config get-value project)

#Creating the secret
gcloud secrets create "MONGODB_URI" \
--project "${PROJECT_ID}" \
--replication-policy "automatic" \
--data-file - <<< "mongodb+srv://danielezeh3:6MriYlRBrJjRywyK@mongo-to-bq.y4ntr.mongodb.net/"

# Creating the secret
gcloud secrets create "MONGO_CLUSTER" \
--project "${PROJECT_ID}" \
--replication-policy "automatic" \
--data-file - <<< "mongo-to-bq"

# Creating the secret
gcloud secrets create "MONGO_DATA_BASE" \
--project "${PROJECT_ID}" \
--replication-policy "automatic" \
--data-file - <<< "customers"

# Creating the secret
gcloud secrets create "PROJECT_ID" \
--project "${PROJECT_ID}" \
--replication-policy "automatic" \
--data-file - <<< "trying-pubsub-2024"

# Creating the secret
gcloud secrets create "TOPIC_ID1" \
--project "${PROJECT_ID}" \
--replication-policy "automatic" \
--data-file - <<< "change-stream-update"


# #Giving the proper authorization
# gcloud secrets add-iam-policy-binding "MONGODB_URI" \
# --project "${PROJECT_ID}" \
# --member "serviceAccount:34188081344-compute@developer.gserviceaccount.com" \
# --role "roles/secretManager.secretAccessor"

