#!/bin/bash

clipboard=$(xclip -o -selection clipboard)
echo "Searching for: $clipboard"
open "http://www.google.com/search?q=$clipboard"
