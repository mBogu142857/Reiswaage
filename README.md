Project: Reiswaage
Author: Martin Boguslawski
last update: 23/07/2021

This project shares an app that guides you through a data acquisition series of a Reiswaage measurement, giving live feedback to the current resultings, and suggests an effective measuring strategy for the selected conditions. The individual measurements can be skipped, corrected, and re-taken by manual selection.

But what is a Reiswaage measurement? 
Usually, one takes a measurement value of an element with a measuring device, where the result is limited by the device's reading precision. E.g. a mass is measured with a scale with a certain precision. If you have a bunch of elements to be measured, let's say n, you cannot be more precise than the reading precision for an individual measurement. The Reiswaage approach considers numerous combinations of the n elements, where for one combination the sum of the elements considered is determined. The final outcome is an estimate for the values for each of the elements. 
You might ask: What is the benefit of this approach? With this method, the error of your estimate underruns the reading precision of the device you are using! The more effort you invest, the more precise will be your estimate. Say, you have n = 8 mass elements to be weighed. You could do 8 individual measurements and end up with the reading precision of the scale. Applying the Reiswaage approach, you can perform up to 2^8 = 256 measurements as this is the number of different combinations of the 8 elements. That's exactly where the name Reiswaage (german for rice scale) comes from: You could turn every scale into a rice scale - and with the appropriate effort even with high precision!
More details on the method together with analytical considerations supported by simulations that allow founded statistical statements will be published soon in a scientific paper.

How does the app work?
Before starting the measurement series, some parameters have to be defined beforehand:
	- 	'total elements' - enter the total number of elements to be measured into the field
	- 	'offset element' - you can choose whether an offset element should be considered or not
	- 	'estimated device precision' - set the estimated/indicated precision of the measuring device.
	-	'n CHOOSE k strategy' - select the strategy for your acquisition campaign, either n choose k (n: total elements available, k: elements considered for one measurement), or all elements to perform all possible 2^n measurements

Select 'Start' to begin the acquisition with the first measurement:
When the value for the first measurement is determined, enter it to the field 'measured weight' and confirm by enter key.
The second measurement is selected in the binary list automatically, where each binary number stands for one element to be measured.
'0' indicates that the element is not considered, '1' shows that the element contributes to the current result.
The leading index shows the number of the current measurement.
The lists 'add element(s)' and 'remove element(s)' give the elements that have to be exchanged from the last to the currently selected measurement.
The field above the 'remove element(s)' window lists the elements of the last measurement performed.
The progress of the acquisition campaign is indicated by the bottom middle gauge next to the binary list of elements.

The three figures on the right-hand side indicate the current results and analysis:
	- top diagramme - residuals of each element's value against the number of measurements to be performed, the title indicates the current estimation of the element's values.
	- middle diagramme - difference of the first estimation to the currently estimated values for each element.
	- bottom diagramme - residuals plotted against the total value taken for one measurement.

When all measurements were performed or in an intermediate state, the results can be stored via the 'Save' button as .csv or .xlsx file.
A measurement series can be re-set by the red-circle-arrow button in the top middle area.