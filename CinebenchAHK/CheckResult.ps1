If (!(Get-Content "BenchmarkResults.txt")) {
 "Benchmark file does not exist."
} else {
 "Benchmark file exists."
 If ( ((Get-Content "BenchmarkResults.txt").Length) -eq 5){
	"Contains correct amount of lines"
 } else {
	"Does not contain correct amount of lines"
 }
}