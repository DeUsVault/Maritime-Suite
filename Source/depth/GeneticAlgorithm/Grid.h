#pragma once
#include <string>
#include <vector>
#include "Point.h"

using namespace std;

class Grid
{
public:
	vector<vector<float>> heightmap;
	vector<vector<int>> landSeaMap;
	vector<vector<int>> grid;
	vector<vector<int>> initial_grid;

	vector<int> radii;
	vector<int> landSea;
	vector<int> costs;

	Grid();
	Grid(TArray<TArray<float>> heightmap_file, TArray<TArray<float>> initial_grid, string radars_file);

	void PrintHeightmap();
	void PrintLandSeaMap();
	void AllocateCoverageMap();
	void ClearCoverageMap();
	void UpdateGrid(int x, int y, int v);
	int SumCoverageMap();
	void PrintCoverageMap();

	void RadarLine(int x1, int y1, int x2, int y2);
	void AddRadarCoverage(int x, int y, int r, int isLand);
	int ComputeCoverage(vector<Point> radarPositions, vector<bool> useRadars);
	double ComputeCoveragePercentage(vector<Point> radarPositions, vector<bool> useRadars);
	int IsRadarOnLand(Point radarPos);
	bool IsRadarOutOfBounds(Point radarPos);
};

