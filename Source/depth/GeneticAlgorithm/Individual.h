#pragma once
#include <vector>
#include "Point.h"
#include "Grid.h"

typedef unsigned int uint;

using namespace std;

class Individual
{
public:
	double fitness;
	double coverage_weight;
	double cost_weight;
	int max_radars;
	int min_radars;
	vector<uint> genes;
	size_t totalRadars;
	uint geneSize;
	uint areaSize;
	Grid* grid;

	Individual();

	Individual(vector<Point> radarPositions, vector<bool> useRadars, uint areaSize, Grid* _grid, double _coverage_weight, double _cost_weight, int _max_radars_to_use, int _min_radars_to_use);

	Point GetRadarPosition(int i);
	bool GetUseRadar(int i);
	vector<Point> GetRadarPositions();
	vector<bool> GetUseRadars();
	double NormalizeCost(int cost, int max_cost);
	double ComputeTotalCost();
	double NormalizeTotalNumRadarsUsed();

	void CalculateFitness();
};
