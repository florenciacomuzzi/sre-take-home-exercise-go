package main

import (
	"bytes"
	"encoding/json"
	"fmt"
	"io/ioutil"
	"log"
	"net/http"
	"os"
	"time"

	"gopkg.in/yaml.v3"
)

type Endpoint struct {
	Name    string            `yaml:"name"`
	URL     string            `yaml:"url"`
	Method  string            `yaml:"method"`
	Headers map[string]string `yaml:"headers"`
	Body    string            `yaml:"body"`
}

type Stats struct {
	Success int
	Total   int
	URL     string
}

func (s *Stats) UptimePercentage() float64 {
	return (float64(s.Success) / float64(s.Total)) * 100

}

func (s *Stats) logResults() {
	percentage := s.UptimePercentage()
	fmt.Printf("%s has %f%% availability\n", s.URL, percentage)
}

func (c *Endpoint) IsUp(ds *Stats) bool {
	if c.URL != ds.URL {
		log.Fatalf("expected %s got stats for %s\n", c.URL, ds.URL)
	}
	bodyBytes, err := json.Marshal(c.Body)
	if err != nil {
		log.Fatal("invalid body")
	}
	reqBody := bytes.NewReader(bodyBytes)

	method := c.Method
	if method == "" {
		method = "GET"
	}

	req, err := http.NewRequest(method, c.URL, reqBody)
	if err != nil {
		return false
	}

	for k, v := range c.Headers {
		req.Header.Set(k, v)
	}

	client := http.Client{
		Timeout: 5 * time.Second,
	}

	start := time.Now()
	resp, err := client.Do(req)
	duration := time.Since(start)
	ds.Total++
	ms := float64(duration.Milliseconds())

	if err == nil && ms < 500 && resp.StatusCode >= 200 && resp.StatusCode < 300 {
		ds.Success++
		return true
	}
	defer resp.Body.Close()
	return false
}

func monitorEndpoints(endpoints []Endpoint) {
	var statz = make(map[string]*Stats)
	for _, endpoint := range endpoints {
		if statz[endpoint.URL] == nil {
			statz[endpoint.URL] = &Stats{URL: endpoint.URL}
		}
	}

	for {
		for _, endpoint := range endpoints {
			stat := statz[endpoint.URL]
			if endpoint.IsUp(stat) {
				fmt.Printf("%s is UP\n", endpoint.Name)
			} else {
				fmt.Printf("%s is DOWN\n", endpoint.Name)
			}
			stat.logResults()
		}

		//time.Sleep(15 * time.Second)
	}
}

func main() {
	if len(os.Args) < 2 {
		log.Fatal("Usage: go run main.go <config_file>")
	}

	filePath := os.Args[1]
	data, err := ioutil.ReadFile(filePath)
	if err != nil {
		log.Fatal("Error reading file:", err)
	}

	var endpoints []Endpoint
	if err := yaml.Unmarshal(data, &endpoints); err != nil {
		log.Fatal("Error parsing YAML:", err)
	}

	monitorEndpoints(endpoints)
}
