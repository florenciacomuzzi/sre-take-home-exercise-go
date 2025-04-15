package main

import (
	"bytes"
	"encoding/json"
	"fmt"
	"io/ioutil"
	"log"
	"math"
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

type DomainStats struct {
	Success int
	Total   int
}

var stats = make(map[string]*DomainStats)

func (c *Endpoint) IsUp(ds *DomainStats) bool {
	bodyBytes, err := json.Marshal(c)
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
	for _, endpoint := range endpoints {
		if stats[endpoint.URL] == nil {
			stats[endpoint.URL] = &DomainStats{}
		}
	}

	for {
		for _, endpoint := range endpoints {
			if endpoint.IsUp(stats[endpoint.URL]) {
				fmt.Printf("%s is UP\n", endpoint.Name)
			} else {
				fmt.Printf("%s is DOWN\n", endpoint.Name)
			}
		}
		logResults()
		time.Sleep(15 * time.Second)
	}
}

func logResults() {
	for domain, stat := range stats {
		percentage := int(math.Round(100 * float64(stat.Success) / float64(stat.Total)))
		fmt.Printf("%s has %d%% availability\n", domain, percentage)
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
