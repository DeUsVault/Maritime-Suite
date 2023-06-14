#pragma once

typedef unsigned int uint;

class Point
{
public:
	uint x;
	uint y;

	Point()
	{
		x = 0;
		y = 0;
	}

	Point(uint _x, uint _y)
	{
		x = _x;
		y = _y;
	}
};

