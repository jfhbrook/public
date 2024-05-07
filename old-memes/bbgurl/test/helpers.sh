#!/usr/bin/env bash

SERVER="const http = require('http');
const fs = require('fs');

const server = http.createServer((req, res) => {
  const headers = req.headers;

  res.setHeader('Content-Type', 'application/json');
  res.end(JSON.stringify({
    headers
  }));
});

server.listen(3000, () => {
  fs.writeFileSync('READY', 'READY');
});"

GET_HEADER="const [ res, header ] = process.argv.slice(1);

const headers = JSON.parse(res).headers;

console.log(headers[header]);"

SERVER_PID=''

function start-server {
  node -e "${SERVER}" &
  SERVER_PID=$!

  while [ ! -f READY ]; do
    sleep 0.1
  done

  rm READY
}

function stop-server {
  kill "${SERVER_PID}"
}

function get-header {
  node -e "${GET_HEADER}" "$@"
}
