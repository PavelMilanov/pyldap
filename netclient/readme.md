1) GOOS=windows GOARCH=amd64 go build .
2) cmd in root priveleges
3) Sc create MyService binPath=C:\MyService\MyService.exe DisplayName=″My New Service″ type=own start=auto
