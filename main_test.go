package main

import (
	"net/http"
	"net/http/httptest"
	"testing"
	"time"
)

func TestIsUp(t *testing.T) {
	tests := []struct {
		name           string
		handler        http.HandlerFunc
		expectUp       bool
		expectedStatus int
	}{
		{
			name: "fast 200 OK",
			handler: func(w http.ResponseWriter, r *http.Request) {
				w.WriteHeader(http.StatusOK)
			},
			expectUp: true,
		},
		{
			name: "slow 200 OK",
			handler: func(w http.ResponseWriter, r *http.Request) {
				time.Sleep(600 * time.Millisecond)
				w.WriteHeader(http.StatusOK)
			},
			expectUp: false,
		},
		{
			name: "400 Bad Request",
			handler: func(w http.ResponseWriter, r *http.Request) {
				w.WriteHeader(http.StatusBadRequest)
			},
			expectUp: false,
		},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			url := "http://invalid"
			if tt.handler != nil {
				srv := httptest.NewServer(tt.handler)
				defer srv.Close()
				url = srv.URL
			}

			endpoint := Endpoint{Name: "test", URL: url}
			up := endpoint.IsUp(&DomainStats{})
			if up != tt.expectUp {
				t.Errorf("expected %v, got %v", tt.expectUp, up)
			}
		})
	}
}
