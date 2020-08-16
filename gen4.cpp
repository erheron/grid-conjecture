#include <bitset>
#include <iostream>
#include <map>
#include <unordered_map>
#include <vector>

using mask = uint32_t; // lower 16 bits - 4x4 grid of target points
typedef std::pair<std::pair<short, short>, std::pair<short, short> > rect; //x_ul x_br y_ul y_br
// ul = "upper left", br = "bottom right"
//
std::ostream & operator << (std::ostream & os, const rect & r){
	os << r.first.first << ' ' << r.second.first << ' ' 
	  << r.first.second << ' ' << r.second.second << ' ';
	return os;
}

constexpr mask next(mask m) { // next mask with the same number of bits
    mask b = m & -m, c = m + b;
    return c | (m^c) / b >> 2;
}

constexpr bool is_good(mask m) {
    return m & 0x000f && m & 0x0ff0 && m & 0xf000 && m & 0x1111 && m & 0x6666 && m & 0x8888;
}

constexpr size_t net_cnt = 348; // precomputed number of "good" nets
using net_set = std::bitset<net_cnt>; // set of "good" nets
const net_set full_net_set = ~net_set();

net_set hit_for(mask target) {
    net_set hit;
    size_t idx = 0;
    for (mask m = 0x000f; m <= 0xf000; m = next(m)) if (is_good(m)) hit.set(idx++, m & target);
    return hit;
}

using box_set = uint64_t; // lower 7*7 bits - set of "good" boxes
constexpr box_set box(size_t x, size_t y) { return box_set(1) << (x*7 + y); }
constexpr box_set full_box_set = (box_set(1) << (7*7))-1;

std::unordered_map<box_set, box_set> upsets; // indexed by singleton sets
std::unordered_map<box_set, net_set> hits; // indexed by singleton sets
std::map<size_t, size_t> results;
std::unordered_map<box_set, rect> coords; // extract coordinates of a rectangle

void compute(box_set s, net_set hit, size_t n, box_set current_set) {
    if (hit.none()){
		++results[n];
		for(int i=0; i < 49;i++)
			if(current_set & (1 << i))
				std::cout << coords[box_set(1) << i];
		std::cout << '\n';
	}
    else for (; s; s &= s-1) compute(s & ~upsets.at(s & -s), hit & hits.at(s & -s), n+1, current_set | (s & -s));
}


int main() {
    const mask x_mask[] { 0b0001, 0b1000, 0b0011, 0b0110, 0b1100, 0b0111, 0b1110 };
    const mask y_mask[] { 0x0001, 0x1000, 0x0011, 0x0110, 0x1100, 0x0111, 0x1110 };
	const std::pair<short, short> coordsXY[] = { {3,4}, {0,1}, {2,4}, {0,2}, {1,4}, {0,3} };
    const std::vector<size_t> up[] { {0, 2, 5}, {1, 4, 6}, {2, 5}, {3, 5, 6}, {4, 6}, {5}, {6} };
    for (size_t x = 0; x < 7; ++x) for (size_t y = 0; y < 7; ++y) {
        box_set upset = 0;
        for (size_t i : up[x]) for (size_t j : up[y]) upset |= box(i, j);
        upsets.emplace(box(x, y), upset);
        hits.emplace(box(x, y), hit_for(x_mask[x] * y_mask[y]));
		coords.emplace(box(x,y), std::make_pair(coordsXY[x], coordsXY[y]));
    }
    compute(full_box_set, full_net_set, 0, 0);
    for (auto r : results) std::cout << r.first << ": " << r.second << std::endl;
    return 0;
}


