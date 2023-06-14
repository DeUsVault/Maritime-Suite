#include "Individual.h"
#include "GrayCode.h"
#include <iostream>

using namespace std;

Individual::Individual()
{
	totalRadars = 0;
	geneSize = 0;
	areaSize = 0;
}

Individual::Individual(vector<Point> radarPositions, vector<bool> useRadars, uint areaLength, Grid* _grid, double _coverage_weight, double _cost_weight, int _max_radars_to_use)
{
	grid = _grid;
	coverage_weight = _coverage_weight;
	cost_weight = _cost_weight;
	max_radars = _max_radars_to_use;
	min_radars = _min_radars_to_use;

	totalRadars = radarPositions.size();
	geneSize = 2 * sizeof(uint) * 8 + 1; // 32 + 32 + 1 = 65
	genes.reserve(totalRadars * geneSize);
	for (int i = 0; i < totalRadars * geneSize; i++)
		genes.push_back(0);
	areaSize = areaLength;

 	for (int i = 0; i < totalRadars; i++)
	{
		bool useRadar = useRadars[i];
		uint x_gray = BinaryToGray(radarPositions[i].x);
		uint y_gray = BinaryToGray(radarPositions[i].y);
		genes[i * geneSize] = useRadar * 1;
		for (uint j = 1; j < (geneSize - 1) / 2; j++)
		{
			genes[i * geneSize + j] = get_bit(x_gray, j - 1);
			genes[i * geneSize + (geneSize - 1) / 2 + j] = get_bit(y_gray, j - 1);
		}
	}
}

Point Individual::GetRadarPosition(int i)
{
	uint x_gray = 0;
	uint y_gray = 0;
	for (uint j = 1; j < (geneSize - 1) / 2; j++)
	{
		set_bit(x_gray, j - 1, genes[i * geneSize + j]);
		set_bit(y_gray, j - 1, genes[i * geneSize + (geneSize - 1) / 2 + j]);
	}
	Point p;
	p.x = GrayToBinary(x_gray);
	p.y = GrayToBinary(y_gray);
	return p;
}

bool Individual::GetUseRadar(int i)
{
	return genes[65 * i] == 1;
}

vector<Point> Individual::GetRadarPositions()
{
	vector<Point> radarPositions;
	for (int i = 0; i < totalRadars; i++)
		radarPositions.push_back(GetRadarPosition(i));
	return radarPositions;
}

vector<bool> Individual::GetUseRadars()
{
	vector<bool> usedRadars;
	for (int i = 0; i < totalRadars; i++)
		usedRadars.push_back(GetUseRadar(i) && !grid->IsRadarOutOfBounds(GetRadarPosition(i)) && (grid->IsRadarOnLand(GetRadarPosition(i)) == grid->landSea[i]));
	return usedRadars;
}

double Individual::NormalizeCost(int cost, int max_cost)
{	
	int min_cost = 0;
	double cost_range = (max_cost - min_cost);
	double coverage_range = (100 - 0);
	double normalized_cost = (((cost - min_cost) * coverage_range) / cost_range) + 0;
	return normalized_cost;
}

double Individual::ComputeTotalCost()
{	
	vector<bool> useRadars = GetUseRadars();
	int sum_of_costs = 0;
	int max_cost = 0;
	for (int i = 0; i < useRadars.size(); i++)
	{ 
		max_cost += costs[i];
		if (useRadars[i])
			sum_of_costs += costs[i];
	}
	double normalized_cost = NormalizeCost(sum_of_costs, max_cost);
	return normalized_cost;
}

int Individual::GetTotalNumRadarsUsed()
{
	vector<bool> usedRadars = GetUseRadars();
	int sum = 0;
	for (int i = 0; i < totalRadars; i++)
		sum += (int)usedRadars[i];
	return sum;
}

double Individual::ComputeTotalRadarsUsedPenalty(int total_radars_used)
{
	double radars_used_penalty = 0;
	if (total_radars_used > max_radars)
	{
		double excess_radars_used = total_radars_used - max_radars;
		double max_excess_radars_used = totalRadars - max_radars;
		radars_used_penalty = excess_radars_used / max_excess_radars_used * 100;
	}
	else if (total_radars_used < min_radars)
	{
		double lack_radars = min_radars - total_radars_used;
		radars_used_penalty = lack_radars / min_radars * 100;
	}
	return radars_used_penalty;
}

void Individual::CalculateFitness()
{
	vector<Point> radarPositions = GetRadarPositions();
	vector<bool> useRadars = GetUseRadars();
	double total_radars_used = GetTotalNumRadarsUsed();

	double coverage = grid->ComputeCoveragePercentage(radarPositions, useRadars);
	double total_cost = ComputeTotalCost();
	double total_radars_used_penalty = ComputeTotalRadarsUsedPenalty(total_radars_used);

	coverage_weight = 1 - cost_weight;
	radars_used_weight = 0.5;
	//min_radars_used_weight = 0.25;
	//coverage_weight = 0.8;
	//coverage_weight = 1.0;
	//cost_weight = 1 - coverage_weight;
	// fitness is a weighted sum of coverage and cost
	// We give a large weight to coverage and a small weight to cost since we want to maximize the coverage and minimize the cost
	fitness = (coverage_weight * coverage) - (cost_weight * total_cost) - (radars_used_weight * total_radars_used_penalty);
}
