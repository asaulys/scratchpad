package handlers
import (
    "deploy-go/models"
    "net/http"
    "encoding/json"
)

// A handler to fetch all the jobs
func GetJobs(w http.ResponseWriter, r *http.Request) {
    // make a slice to hold our jobs data
    var jobs []models.Job
    // add some job to the slice
    jobs = append(jobs, models.Job{ID: 1, Name:"Accounting"})
    jobs = append(jobs, models.Job{ID: 2, Name:"Programming"})
    w.Header().Set("Content-Type", "application/json")
    json.NewEncoder(w).Encode(jobs)
}
