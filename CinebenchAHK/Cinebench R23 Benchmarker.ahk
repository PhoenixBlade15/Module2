#z::

 ; Run Cinebench
Run, Cinebench, , Max									; Runs Cinebench R23 in maximized
Sleep, 6000 										; Sleeps for 20 seconds for program to open

 ; Run Benchmarks
MouseMove, 350, 165, 10									; Moves mouse over to Multi Core benchmark
MouseClick, Left, 350, 165, 1, U,							; Clicks to begin Multi Core benchmark
Sleep, 900000										; Sleeps for 15 minutes to give cinebench test to run
				
MouseMove, 350, 200, 10									; Moves mouse over to start Single Core benchmark
MouseClick, Left, 350, 200, 1, U,							; Clicks to begin Single Core benchmark
Sleep, 900000										; Sleeps for 15 minutes to give cinebench test to run

  ; Put processor into text doc
MouseMove, 350, 300, 10									; Moves mouse over to Processor Section
Sleep, 700
MouseClick, Right, 350, 300, 1, U,							; Right clicks the Processor Section
Sleep, 1000										; Sleeps for a bit to let program catch up
MouseMove, 375, 310, 10									; Moves the mouse to the Processor copy button
Sleep, 700
MouseClick, Left, 375, 310, 5, U,							; Copies the Processor Section
Sleep, 1000										; Sleeps for a bit to let program catch up
processor := clipboard 									; Sets output to the processor information
FileAppend, Processor is: %processor% `n, BenchmarkResults.txt, 			; Appends the processor information to the text file

  ; Put number of cores into text doc
MouseMove, 350, 350, 10									; Moves mouse over to Cores x GHz Section
Sleep, 700
MouseClick, Right, 350, 350, 1, U,							; Right clicks the Cores x GHz Section
Sleep, 1000										; Sleeps for a bit to let program catch up
MouseMove, 375, 360, 10									; Moves the mouse to the Cores x GHz copy button
Sleep, 700
MouseClick, Left, 375, 360, 5, U,							; Copies the Cores x GHz Section
Sleep, 1000										; Sleeps for a bit to let program catch up
numberCores := SubStr(clipboard,1,1) 							; Sets information in a string variable
FileAppend, Number of Cores: %numberCores% `n, BenchmarkResults.txt, 			; Appends the cores information to the text file

  ; Put Multi Core score into text doc
MouseMove, 300, 165, 10									; Moves mouse over to Multi Core Score section
Sleep, 700
MouseClick, Right, 300, 165, 1, U,							; Right clicks the Multi Core Score section
Sleep, 1000										; Sleeps for a bit to let program catch up
MouseMove, 325, 175, 10									; Moves the mouse to the Multi Core Score copy button
Sleep, 700
MouseClick, Left, 325, 175, 5, U,							; Copies the Multi Core Score section
Sleep, 1000										; Sleeps for a bit to let program catch up
multiCoreScore := clipboard 								; Sets information in a string variable
FileAppend, Multi Core Score: %multiCoreScore% `n, BenchmarkResults.txt, 		; Appends the multi core score information to the text file

  ; Put Single Core score into text doc
MouseMove, 300, 200, 10									; Moves mouse over to Multi Core Score section
Sleep, 700
MouseClick, Right, 300, 200, 1, U,							; Right clicks the Multi Core Score section
Sleep, 1000										; Sleeps for a bit to let program catch up
MouseMove, 325, 210, 10									; Moves the mouse to the Multi Core Score copy button
Sleep, 700
MouseClick, Left, 325, 210, 5, U,							; Copies the Multi Core Score section
Sleep, 1000										; Sleeps for a bit to let program catch up
singleCoreScore := clipboard 								; Sets information in a string variable
FileAppend, Single Core Score: %singleCoreScore% `n, BenchmarkResults.txt, 		; Appends the multi core score information to the text file

  ; Estimate Single Core score by Multi Core Score / # of cores
Sleep, 700
estimatedSingleScore := multiCoreScore / numberCores
FileAppend, Estimated Single Core Score: %estimatedSingleScore%, BenchmarkResults.txt

  ; Take a screenshot of the results
Sleep, 700
Run, SnippingTool, , Max								; Runs Snipping Tool to take screenshot
Sleep, 700										
WinActivate, Snipping Tool, , , 							; Makes Snipping Tool in focus
Send ^N											; Creates a new Snip
Sleep, 1000										
MouseClickDrag, Left, -10000, -10000, 10000, 10000, 10, R				; Drags the snip to encase the entire screen
Sleep, 700
Send ^s											; Tells Snipping Tool to save
Send BenchmarkScreenshot								; Enters the name of the screenshot
Send {enter}										; Confirms the save

Send !{f4}
Send !{f4}
return