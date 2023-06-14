#include "Population.h"
#include <iostream>

using namespace std;

Population::Population()
{
	populationSize = 0;
	totalRadars = 0;
	areaSize = 0;
}

Population::Population(int size, int radarCount, int areaLength, Grid* _grid, double _coverage_weight, double _cost_weight, int _max_radars_to_use, int _min_radars_to_use)
{
	grid = _grid;
	populationSize = size;
	totalRadars = radarCount;
	areaSize = areaLength;
	InitializeRandomPopulation(_coverage_weight, _cost_weight, _max_radars_to_use, _min_radars_to_use);
}

void Population::InitializeRandomPopulation(double _coverage_weight, double _cost_weight, int _max_radars_to_use)
{
	std::random_device rd;
	std::mt19937 gen(rd());
	std::uniform_int_distribution<> distr(0, areaSize);
	vector<Point> radarPositions;
	vector<bool> useRadars;
	for (int i = 0; i < populationSize; i++)
	{
		for (int j = 0; j < totalRadars; j++)
		{
			Point p;
			p.x = distr(gen);
			p.y = distr(gen);
			radarPositions.push_back(p);
			useRadars.push_back(true);
		}
		Individual new_individual(radarPositions, useRadars, areaSize, grid, _coverage_weight, _cost_weight, _max_radars_to_use);
		individuals.push_back(new_individual);
		radarPositions.clear();
		useRadars.clear();
	}
	geneSize = individuals[0].geneSize;
}

int Population::GetFittestIndex()
{
	double maxFitness = 0.0;
	int maxFitnessIndex = 0;
	for (int i = 0; i < individuals.size(); i++)
	{
		if (individuals[i].fitness >= maxFitness)
		{
			maxFitness = individuals[i].fitness;
			maxFitnessIndex = i;
		}
	}
	fitness = maxFitness;
	return maxFitnessIndex;
}

Individual Population::GetFittest()
{
	return individuals[GetFittestIndex()];
}

int Population::GetSecondFittestIndex()
{
	int maxFitnessIndex = GetFittestIndex();
	int secondMaxFitnessIndex = 0;
	int secondMaxFitness = 0;
	for (int i = 0; i < individuals.size(); i++)
	{
		if (individuals[i].fitness >= secondMaxFitness && i != maxFitnessIndex)
		{
			secondMaxFitnessIndex = i;
			secondMaxFitness = individuals[i].fitness;
		}
	}
	return secondMaxFitnessIndex;
}

Individual Population::GetSecondFittest()
{
	return individuals[GetSecondFittestIndex()];
}

int Population::GetLeastFittestIndex()
{
	double minFitness = 99.99;
	int minFitnessIndex = 0;
	for (int i = 0; i < individuals.size(); i++)
	{
		if (individuals[i].fitness <= minFitness)
		{
			minFitness = individuals[i].fitness;
			minFitnessIndex = i;
		}
	}
	return minFitnessIndex;
}

Individual Population::GetLeastFittest()
{
	return individuals[GetLeastFittestIndex()];
}

void Population::CalculateFitness()
{
	for (int i = 0; i < individuals.size(); i++)
		individuals[i].CalculateFitness();
	GetFittestIndex();
}