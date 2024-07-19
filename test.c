#include <stdio.h>
#include <stdbool.h>
#include <math.h>
#include <stdlib.h>
#include <time.h>
#include <unistd.h>
// global variables, some should maybe be constants instead
#define timeout 1000000

float e;
float kB;
double nu;
float T;
float bulk_r;
double* energies;
double surface_distance;
double max_time;

// should modify so timeout is passed into the struct or into the kmc loop
struct kmc_data {
    size_t size;
    double times[timeout];
    double distances[timeout];
    bool reached_surface;
};

float get_r(bool direction, int distance) {
    /**
     * return rate of migration either up(0), or down(1), depending on distance
     * distance 0 is when we start to see the strain field!
    */
    float E;
    if (distance >= 0) {
        // should pass in precalculated values to save doing pow everytime
        return nu * pow(e, -energies[2*distance+direction] / (kB * T));
    }
    else {
        return bulk_r;
    }
}

float get_R(int distance) {
    return (get_r(0, distance) + get_r(1, distance));
}

float get_P(bool directon, int distance) {
    return get_r(directon, distance) / get_R(distance);
}

float get_random() {
    return rand() / (RAND_MAX + 1.0);
}

float get_t(int distance) {
    return -log(get_random()) / get_R(distance);
}

// TODO:
// WRITE kmc_loop, then all you have to do is write a python function which
// just processes the data, just store it all in one giant python array
// that's written after the loop is done

struct kmc_data *kmc_loop() {
    // return get_r(0, distance);
    struct kmc_data *data = malloc(sizeof(struct kmc_data)); 
    data->times[0] = 0;
    data->distances[0] = 0;
    data->reached_surface = 0;
    for (int i = 1; i < timeout; i++) {
        double last_distance = data->distances[i-1];
        double last_time = data->times[i-1];

        data->times[i] = last_time + get_t(data->distances[i-1]);

        if (get_random() < get_P(0, last_distance)) {
            data->distances[i] = last_distance + 1;
        } else {
            data->distances[i] = last_distance - 1;
        }
        if (data->distances[i] >= surface_distance) {
            data->size = i;
            data->reached_surface = 1;
            break;
        }
        if (data->times[i] >= max_time || i == timeout) {
            data->size = i;
            break;
        }
    }
    return data;
}

double index_times(struct kmc_data *data, size_t i) {
    return data->times[i];
}

double index_distances(struct kmc_data *data, size_t i) {
    return data->distances[i];
}

size_t get_size(struct kmc_data *data) {
   return data->size;
}

bool get_reached_surface(struct kmc_data *data) {
    return data->reached_surface;
}

void free_kmc(struct kmc_data *data) {
    free(data);
}

int main(double* array) {
    // just defining all the constants at the start, they are NOT technically
    // constant so we can't define them globally normally because
    // a) they rely on functions (pow)
    // b) they rely on each other -> not consant!
    srand(time(NULL) ^ getpid());
    energies = array;
    e = 2.71828;
    kB = 8.6173303 * pow(10, -5);
    T = 800;
    nu = 40 * pow(10, 12); // this might not be a good idea
    bulk_r = nu * pow(e, -2.55/(kB*T));
    surface_distance = 19; //double check
    max_time = 100*3600;
    return 0;
}