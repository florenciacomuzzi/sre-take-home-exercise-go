package main

import (
	"fmt"
	"log"
	"math/rand"
	"net/http"
	"time"
)

func main() {
	rand.Seed(time.Now().UnixNano())

	http.HandleFunc("/", func(w http.ResponseWriter, r *http.Request) {
		if rand.Intn(2) == 0 { // 50% chance to return 500
			http.Error(w, "Internal Server Error", http.StatusInternalServerError)
			log.Println("Returned 500")
			return
		}

		w.WriteHeader(http.StatusOK)
		fmt.Fprintln(w, "Hello, World!")
		log.Println("Returned 200")
	})

	port := "8080"
	log.Printf("Starting server on port %s...\n", port)
	err := http.ListenAndServe(":"+port, nil)
	if err != nil {
		log.Fatalf("Server failed to start: %v", err)
	}
}
