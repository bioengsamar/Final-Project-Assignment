# Final Project Assignment - Team 19 - SBE309 | DSP

## Team Work

| Name              | Section | Bench |
|-------------------|---------|-------|
| Abdulla A. Zahran | 2       | 5     |
| Kirolos Dawood    | 2       | 15    |
| Bishoy M. Markos  | 1       | 24    |
| Samar Ibrahim     | 1       | 40    |

## Project Description

We agreed as a team to work on the first 4 problems only, here's the full description of our assignment and short notes on results.

### Problem #1

Working on Covid-19 Pandemic statistics was quite hard in the first time but we managed to manipulate and use different code blocks quoted from different projects to do what is required but we had some problems unfortunately so we may say we did 75% ~ 80% of the job.

We used online source of data from official source by the Center for Systems Science and Engineering (CSSE) at Johns Hopkins University updated every day applied on each map/graph.

- The part of GUI is not ready for this problem due to lack of time.
- Exporting the results to video/GIF also is not done also -except part C-.

We wish that we had more time to complete this task 100%.

#### P.1 Part A

The animated bubble graph was generated on notebook successfully but we have a problem with the bubble size maybe it has different way to code it, we were able to manage the imported data successfully.

![Buble Graph](/Problem_1/ScreenShots/Annotation%202020-06-01%20235016.png)

#### P.1 Part B

This part done 100% we have generated the colored map with slider and animation on Jupyter Notebook. (you can export the output to HTML file too.)

![Colored Map](/Problem_1/ScreenShots/Annotation%202020-06-01%20235051.png)

#### P.1 Part C

For the animated sorted chart we did the required 100% and generated GIFs for the results.

![Confirmed Cases](/Problem_1/GIFs/confirmed_covid2.gif)

![Deaths](/Problem_1/GIFs/Deaths_covid2.gif)

#### P1. Part D

Still Working...

### Problem #2

As the required is to design a decoder for JPEG format we were able to manage a library called *TurboJPEG* it has simple decoder within its code. So, we adding a parameter on the calling function of the decoder to pass the percentage of data that would be decoded on each step then it returns the decoded portion of data as required.

![JPEG](/Problem_2/ScreenShots/Annotation%202020-05-29%20203950.png)

![JPEG](/Problem_2/ScreenShots/Annotation%202020-05-29%20204015.png)

![JPEG](/Problem_2/ScreenShots/Annotation%202020-05-29%20204030.png)

### Problem #3

It's required to design and implement two different musical instruments, we worked on Piano and Guitar through some equations that generate similar sound of these instruments.

![Musical Instrument](/Problem_3/ScreenShots/Annotation%202020-05-18%20235206.png)

![Musical Instrument](/Problem_3/ScreenShots/Annotation%202020-05-18%20235305.png)

### Problem #4

Using two different ways to did the separation we did the required.

#### P4. Part A

Using *Librosa* we did the separation job for this part and giving two different sounds the first one for Vocals and the second one for Music Only.

![Song Separation](/Problem_4/ScreenShots/Annotation%202020-05-29%20175702.png)

#### P4. Part B

We worked on two different types of mixtures a Coctail Party and Signal Analyzer.

The coctail party method is to mix 2 ~ n different sources of sounds (we set n = 5) with different wieghts then separate that mixture.

![Coctail Party](/Problem_4/ScreenShots/Annotation%202020-05-29%20175758.png)

The signal analysis is by import any data i.e we used normal ECG, then adding some noise as arrhythmia then separate each component.

![Signal Analyzer](/Problem_4/ScreenShots/Annotation%202020-05-29%20180019.png)
