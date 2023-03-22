package main

import (
    "deploy-go/handlers"
    "log"
    "net/http"
    "github.com/go-chi/chi"
)

func main() {

  router := chi.NewRouter()
  router.Get("/api/jobs", handlers.GetJobs)
  // run it on port 12345
  err := http.ListenAndServe("0.0.0.0:12345", router)
  if err != nil {
    log.Fatal(err)
  }
}
