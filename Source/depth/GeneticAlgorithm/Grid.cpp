#include "Grid.h"
#include "Containers/Array.h"
#include <fstream>
#include <iostream>
#include <sstream>
#include <cmath>
#include <math.h>

using namespace std;

Grid::Grid() {}

Grid::Grid(TArray<TArray<float>> heightmap_file, TArray<TArray<int>> initial_grid, string radars_file)
{
	string line;
	string word;
	//fstream fin_h;
	//fin_h.open(heightmap_file, ios::in);

	/*if (!fin_h.is_open())
	{
		cout << "Heightmap file " << heightmap_file << " not found." << endl;
		return;
	}*/


	//vector<float> heightmap_row;
	//vector<int> landSeaMap_row;

	/*while (fin_h)
	{
		getline(fin_h, line);
		stringstream s(line);
		while (getline(s, word, ','))
		{
			float h = stof(word);
			heightmap_row.push_back(h);
			landSeaMap_row.push_back(h != 0);
		}

		if (heightmap_row.size() != 0)
		{
			heightmap.push_back(heightmap_row);
			landSeaMap.push_back(landSeaMap_row);
		}

		heightmap_row.clear();
		landSeaMap_row.clear();
	}*/

	vector<float> heightmap_row;
	vector<int> landSeaMap_row;
	for (const TArray<float>& row : heightmap_file)
	{
		for (float h : row)
		{
			heightmap_row.push_back(h);
			landSeaMap_row.push_back(h != 0);
		}

		if (!heightmap_row.empty())
		{
			heightmap.push_back(heightmap_row);
			landSeaMap.push_back(landSeaMap_row);
		}

		heightmap_row.clear();
		landSeaMap_row.clear();
	}
	AllocateCoverageMap();

	vector<int> initial_grid_row;
	for (const TArray<int>& row : initial_grid)
	{
		for (int g : row)
			initial_grid_row.push_back(g);
		initial_grid.push_back(initial_grid_row);
		initial_grid_row.clear();
	}

	fstream fin_r;
	fin_r.open(radars_file, ios::in);

	if (!fin_r.is_open())
	{
		cout << "Radars file " << radars_file << " not found." << endl;
		return;
	}

	while (getline(fin_r, line))
	{
		stringstream s(line);
		int c = 0;
		while (getline(s, word, ','))
		{
			if (c == 0)
				radii.push_back(stoi(word));
			if (c == 1)
				landSea.push_back(stoi(word));
			if (c == 2)
				costs.push_back(stoi(word));
			c++;
		}
	}

}

void Grid::PrintHeightmap()
{
	for (int i = 0; i < heightmap.size(); i++)
	{
		for (int j = 0; j < heightmap[i].size(); j++)
			cout << heightmap[i][j] << " ";
		cout << endl;
	}
}

void Grid::PrintLandSeaMap()
{
	for (int i = 0; i < landSeaMap.size(); i++)
	{
		for (int j = 0; j < landSeaMap[i].size(); j++)
			cout << landSeaMap[i][j] << " ";
		cout << endl;
	}
}

void Grid::AllocateCoverageMap()
{
	for (int i = 0; i < heightmap.size(); i++)
	{
		vector<int> grid_row;
		for (int j = 0; j < heightmap[i].size(); j++)
			grid_row.push_back(0);
		grid.push_back(grid_row);
	}
}

void Grid::ClearCoverageMap()
{
	for (int i = 0; i < grid.size(); i++)
		for (int j = 0; j < grid[i].size(); j++)
			grid[i][j] = initial_grid[i][j];
}

void Grid::UpdateGrid(int x, int y, int v)
{
	grid[y][x] = v;
	//PrintCoverageMap();
}

int Grid::SumCoverageMap()
{
	int s = 0;
	for (int i = 0; i < grid.size(); i++)
		for (int j = 0; j < grid.size(); j++) 
			s += grid[i][j];
		
	return s;
}

void Grid::PrintCoverageMap()
{	
	int counter = 0;
	for (int i = 0; i < grid.size(); i++)
	{
		for (int j = 0; j < grid.size(); j++){ 
			cout << grid[i][j] << " ";
			if (grid[i][j] == 1)
				counter = counter + 1;
		}
		cout << endl;
	}

}

float dist_sq(int x0, int y0, int x1, int y1)
{
	return (x1 - x0) * (x1 - x0) + (y1 - y0) * (y1 - y0);
}


void Grid::RadarLine(int x0, int y0, int x1, int y1)
{
	int dx = abs(x1 - x0);
	int sx = x0 < x1 ? 1 : -1;
	int dy = -abs(y1 - y0);
	int sy = y0 < y1 ? 1 : -1;
	int error = dx + dy;

	int x0_init = x0;
	int y0_init = y0;
	int areaSize = heightmap.size();
	int distance_from_init_position = 0;

	double pi = 3.14159265359;
	double angle_degrees = 83;
	double angle_rad = (angle_degrees * (pi / 180));

	while (1)
	{	
		distance_from_init_position += 1;
		// Apply some trigonometry here to find the height the radar can see at each "cell"
		// 180 - 90 - 7 = 83 degrees
		// 7 degrees is the angle of the radar's beam
		double sin_angle = sin(angle_rad);
		double cos_angle = cos(angle_rad);
		double hypotenuse = distance_from_init_position / sin_angle; 

		// We multiply by 1000 to get the distance in meters
		double height_cutoff = (hypotenuse * cos_angle) * 1000;

		if (x0 >= areaSize || y0 >= areaSize || x0 < 0 || y0 < 0)
			// Out of bounds !
			break;
		if (heightmap[x0][y0] > heightmap[x0_init][y0_init] + height_cutoff)
			// And also check that the height of the cell is not greater than what the radar can see at that distance based on its beam.
			break;

		UpdateGrid(x0, y0, 1);

		if (x0 == x1 && y0 == y1)
			break;
		int e2 = 2 * error;
		if (e2 >= dy)
		{
			if (x0 == x1)
				break;
			error = error + dy;
			x0 = x0 + sx;
		}
		if (e2 <= dx)
		{
			if (y0 == y1)
				break;
			error = error + dx;
			y0 = y0 + sy;
		}
	}
}

void Grid::AddRadarCoverage(int x_center, int y_center, int r, int isLand)
{
	int x = r, y = 0;

	if (x_center >= landSeaMap.size() || y_center >= landSeaMap.size() || x_center < 0 || y_center < 0)
		return;

	if (landSeaMap[x_center][y_center] != isLand)
		return;

	UpdateGrid(x_center, y_center, 1);

	RadarLine(x_center, y_center, x + x_center, y + y_center);
	RadarLine(x_center, y_center, -x + x_center, y + y_center);
	RadarLine(x_center, y_center, y + x_center, x + y_center);
	RadarLine(x_center, y_center, y + x_center, -x + y_center);

	int P = 1 - r;
	while (x > y)
	{
		y++;

		if (P <= 0)
			P = P + 2 * y + 1;
		else
		{
			x--;
			P = P + 2 * y - 2 * x + 1;
		}

		if (x < y)
			break;

		RadarLine(x_center, y_center, x + x_center, y + y_center);
		RadarLine(x_center, y_center, -x + x_center, y + y_center);
		RadarLine(x_center, y_center, x + x_center, -y + y_center);
		RadarLine(x_center, y_center, -x + x_center, -y + y_center);

		if (x != y)
		{
			RadarLine(x_center, y_center, y + x_center, x + y_center);
			RadarLine(x_center, y_center, -y + x_center, x + y_center);
			RadarLine(x_center, y_center, y + x_center, -x + y_center);
			RadarLine(x_center, y_center, -y + x_center, -x + y_center);
		}
	}
}

bool Grid::IsRadarOutOfBounds(Point radarPos)
{
	return radarPos.x >= landSeaMap.size() || radarPos.y >= landSeaMap.size() || radarPos.x < 0 || radarPos.y < 0;
}

int Grid::IsRadarOnLand(Point radarPos)
{
	//if (IsRadarOutOfBounds(radarPos))
	//	return -1;
	return landSeaMap[radarPos.x][radarPos.y];
}

int Grid::ComputeCoverage(vector<Point> radarPositions, vector<bool> useRadars)
{
	ClearCoverageMap();
	for (int i = 0; i < radarPositions.size(); i++)
		if (useRadars[i])
			AddRadarCoverage(radarPositions[i].x, radarPositions[i].y, radii[i], landSea[i]);
	int coverage = SumCoverageMap();
	return coverage;
}

double Grid::ComputeCoveragePercentage(vector<Point> radarPositions, vector<bool> useRadars)
{
	ClearCoverageMap();
	for (int i = 0; i < radarPositions.size(); i++)
		if (useRadars[i])
			AddRadarCoverage(radarPositions[i].x, radarPositions[i].y, radii[i], landSea[i]);
	int coverage = SumCoverageMap();

	double coverage_percentage = (1.0 * coverage) / (grid.size() * grid.size()) * 100;

	return coverage_percentage;
}