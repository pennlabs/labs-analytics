package main

import (
	"context"
	"crypto/rand"
	"crypto/sha256"
	"encoding/hex"
	"encoding/json"
	"github.com/redis/go-redis/v9"
	"io"
	"log"
	"net/http"
	"os"
	"os/signal"
	"syscall"
	"time"
)

// Define your API response structure
type ApiResponse struct {
	Message string `json:"message"`
}

// Handler function for your API endpoint
func apiHandler(w http.ResponseWriter, r *http.Request) {
	body, err := io.ReadAll(r.Body)
	if err != nil {
		http.Error(w, "Error reading request body", http.StatusInternalServerError)
		return
	}
	defer r.Body.Close()
	response := ApiResponse{http.StatusText(http.StatusOK)}

	client := redis.NewClient(&redis.Options{
		Addr:     "localhost:6379",
		Password: "",
		DB:       0,
	})
	// Simulate some work using a goroutine
	go func() {
		// Hash the request body
		randBytes := make([]byte, 16)
		_, err := rand.Read(randBytes)
		hash := sha256.New()
		hash.Write(randBytes[:8])
		hashed := hex.EncodeToString(hash.Sum(nil))

		// Fill the slice with random data
		if err != nil {
			log.Println("Error generating random bytes: ", err)
			return
		}

		key := hashed[:8]
		value := body
		// Simulate adding a random hash as key and random hash as value to Redis
		err = client.Set(context.Background(), key, value, 0).Err()
		if err != nil {
			log.Println("Error adding to Redis: ", err)
		} else {
			log.Println("Added to Redis: ", key)
		}
	}()

	w.Header().Set("Content-Type", "application/json")
	json.NewEncoder(w).Encode(response)
}

func main() {
	// Create a new ServeMux and register the handler
	mux := http.NewServeMux()
	mux.HandleFunc("/analytics", apiHandler)

	server := &http.Server{
		Addr:    ":8000",
		Handler: mux,
	}
	// Listen for shutdown signals
	stopChan := make(chan os.Signal, 1)
	signal.Notify(stopChan, os.Interrupt, syscall.SIGTERM)

	go func() {
		<-stopChan // Wait for shutdown signal
		log.Println("Shutting down server...")

		ctx, cancel := context.WithTimeout(context.Background(), 5*time.Second)
		defer cancel()

		server.Shutdown(ctx)
	}()

	log.Println("Starting server on :8000")
	if err := server.ListenAndServe(); err != nil && err != http.ErrServerClosed {
		log.Fatalf("ListenAndServe error: %v", err)
	}

	log.Println("Server gracefully stopped")
}
