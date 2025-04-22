package main

import (
	"io"
	"net/http"
	"net/http/httptest"
	"testing"
	"time"
)

func TestIsUp(t *testing.T) {
	tests := []struct {
		name              string
		method            string
		headers           map[string]string
		body              string
		handler           http.HandlerFunc
		expectUp          bool
		expectBodyCheck   bool
		expectedBody      string
		expectedHeader    string
		expectedHeaderVal string
	}{
		{
			name: "GET 200 OK",
			handler: func(w http.ResponseWriter, r *http.Request) {
				w.WriteHeader(http.StatusOK)
			},
			expectUp: true,
		},
		{
			name: "slow response over 500ms",
			handler: func(w http.ResponseWriter, r *http.Request) {
				time.Sleep(600 * time.Millisecond) // exceeds 500ms limit
				w.WriteHeader(http.StatusOK)
			},
			expectUp: false,
		},
		{
			name:   "POST with JSON body",
			method: "POST",
			headers: map[string]string{
				"Content-Type": "application/json",
			},
			body:              `{"foo":"bar"}`,
			expectUp:          true,
			expectBodyCheck:   true,
			expectedBody:      "{\"foo\":\"bar\"}",
			expectedHeader:    "Content-Type",
			expectedHeaderVal: "application/json",
			handler: func(w http.ResponseWriter, r *http.Request) {
				if r.Method != "POST" {
					t.Errorf("expected POST method, got %s", r.Method)
				}
				if ct := r.Header.Get("Content-Type"); ct != "application/json" {
					t.Errorf("expected Content-Type application/json, got %s", ct)
				}
				body, _ := io.ReadAll(r.Body)
				if string(body) != `"{\"foo\":\"bar\"}"` {
					t.Errorf("expected body '%s', got '%s'", `"{\"foo\":\"bar\"}"`, string(body))
				}
				w.WriteHeader(http.StatusOK)
			},
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

			endpoint := Endpoint{
				Name:    tt.name,
				URL:     url,
				Method:  tt.method,
				Headers: tt.headers,
				Body:    tt.body,
			}

			up := endpoint.IsUp(&Stats{URL: url})
			if up != tt.expectUp {
				t.Errorf("expected IsUp = %v, got %v", tt.expectUp, up)
			}
		})
	}
}
