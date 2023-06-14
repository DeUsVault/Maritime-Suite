#pragma once
#include <iostream>
#include "Population.h"
#include "Individual.h"

using namespace std;

class GeneticAlgorithm
{
public:
	Population population;
	int generation = 0;
	Individual fittest;
	Individual secondFittest;
	int mutationRate;
	int maxGenerations;
	double fitness_target;
	int areaSize;
	int totalRadars;
	Grid grid;

	GeneticAlgorithm(TArray<TArray<float>> heightmap, TArray<TArray<int>> initial_grid, string radars_file, int _maxGenerations, int _populationSize, 
		int _mutationRate, double _fitness_target, double _coverage_weight, double _cost_weight, int _max_radars_to_use, int _min_radars_to_use);

	void Fit();

	vector<Point> GetSolutionRadarPositions();
	vector<bool> GetSolutionUseRadars();
	void DisplayCoverageMap();
	float Coverage();

	float Cost();

	void Selection();

	void CrossOver();

	void Mutation();

	void AddFittestOffspring();
};
