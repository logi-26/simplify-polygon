# simplify-polygon
Python scripts to remove redundant points from a Shapely Polygon object.<br/>

![alt text](https://github.com/logi-26/simplify-polygon/blob/main/image1.png?raw=true)

![alt text](https://github.com/logi-26/simplify-polygon/blob/main/image2.png?raw=true)

## Info
The simplify() method in the Shapely library can be used to get rid of points that may be unncesesary for representing an object.<br/>
It returns a simplified version of the geometry object based on a tolerance.<br/>
If the tolernace is too high the function will remove too many points which will alter the shape of the polygon.<br/>
If the tolerance is too low it will not remove all of the unncesesary points from the polygon.<br/>

I wanted a function that would remove all unncesesary points from the polygon without altering the polygon shape.<br/>
These scripts check the interior angles of the polygon points to eliminate unncesesary points between vertices.<br/>
It then plots the points, displaying the removed points in red and the unchanged points in blue.<br/>

## Usage
Requires Python 3.<br/>
Download or clone this repo.<br/>
Run main.py.<br/>
