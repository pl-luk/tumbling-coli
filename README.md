# tumbling-coli

## Idea:
1. Bacteria object with a unit vector `lookingAt` for the direction in which the bacteria is facing, the position and a `step()` function to calculate a run and tumble
2. loop until certain conditions are met (simulation steps of user interruption)
3. loop through each bacteria and call the step function
4. save the coordinates of each bacteria in a file and update the graphical interface

### Step function
1. Draw a random angle from a uniform? distribution with mean 70°
2. rotate the `lookingAt` vector by that angle
3. Draw a random walking time from the exponential distribution
4. calculate the length of the walk with s = v * t
5. scale `lookingAt` and add it to the position vector to get the new positon
6. update the position vector
