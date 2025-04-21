package main

import (
	"fmt"
	"io"
	"log"
	"math/rand"
	"net/http"
	"os"
	"strconv"
	"time"
)

func main() {
	rand.Seed(time.Now().UnixNano())

	// Get failure percentage from environment variable
	failurePercentStr := os.Getenv("FAILURE_PERCENTAGE")
	if failurePercentStr == "" {
		failurePercentStr = "50" // Default to 50% if not set
	}

	failurePercent, err := strconv.Atoi(failurePercentStr)
	if err != nil || failurePercent < 0 || failurePercent > 100 {
		log.Fatalf("Invalid FAILURE_PERCENTAGE. Must be a number between 0 and 100, got: %s", failurePercentStr)
	}

	http.HandleFunc("/", func(w http.ResponseWriter, r *http.Request) {
		if rand.Float64() * 100 < float64(failurePercent) { // Convert percentage to probability
			http.Error(w, "Internal Server Error", http.StatusInternalServerError)
			log.Println("Returned 500")
			return
		}

		switch r.Method {
		case http.MethodPost:
			body, err := io.ReadAll(r.Body)
			if err != nil {
				http.Error(w, "Error reading request body", http.StatusBadRequest)
				log.Printf("Error reading request body: %v", err)
				return
			}
			log.Printf("Received POST request with body: %s", string(body))
			w.WriteHeader(http.StatusOK)
			fmt.Fprintf(w, "Received POST request with body: %s", string(body))
		case http.MethodGet:
			w.WriteHeader(http.StatusOK)
			fmt.Fprintln(w, "Hello, World!")
		default:
			http.Error(w, "Method not allowed", http.StatusMethodNotAllowed)
			return
		}
		log.Println("Returned 200")
	})

	port := "8080"
	log.Printf("Starting server on port %s...\n", port)
	err = http.ListenAndServe(":"+port, nil)
	if err != nil {
		log.Fatalf("Server failed to start: %v", err)
	}
}
