#include <cassert>
#include <filesystem>
#include <fstream>
#include <iostream>
#include <numeric>
#include <regex>
#include <stdexcept>
#include <string>

#include <fmt/core.h>

namespace fs = std::filesystem;

fs::path DATA_FOLDER = fs::current_path() / ".." / ".." / "data";
fs::path EXAMPLE_DATA_PATH = DATA_FOLDER / "example.dat";
fs::path TEST_DATA_PATH = DATA_FOLDER / "test.dat";

/****************************************************************************************
 * @brief
 *
 * @param fpath:
 * @return std::string:
 ****************************************************************************************/
auto load(const fs::path &fpath) -> std::string {
  std::FILE *fp = std::fopen(fpath.c_str(), "r");
  if (fp) {
    std::string contents;
    std::fseek(fp, 0, SEEK_END);
    contents.resize(std::ftell(fp));
    std::rewind(fp);
    std::fread(&contents[0], 1, contents.size(), fp);
    std::fclose(fp);
    return contents;
  }
  throw(errno);
}

/****************************************************************************************
 * @brief
 *
 * @param input:
 * @param regex:
 * @return std::vector<std::string>:
 ****************************************************************************************/
auto split(const std::string &input, const std::string &pattern)
    -> std::vector<std::string> {
  std::regex re(pattern);
  std::sregex_token_iterator first{input.cbegin(), input.cend(), re, -1}, last;
  return {first, last};
}

/****************************************************************************************
 * @brief
 *
 * @param input:
 * @param regex:
 * @return std::vector<std::string>:
 ****************************************************************************************/
std::vector<uint32_t> to_uint32_vec(const std::vector<std::string> &input) {
  std::vector<uint32_t> output;
  std::transform(input.cbegin(), input.cend(), std::back_inserter(output),
                 [](const std::string &str) { return std::stoi(str); });
  return output;
}

/****************************************************************************************
 * @brief
 *
 * @param str:
 * @return int:
 ****************************************************************************************/
auto solve_pt1(const std::string &text) -> uint64_t {
  std::vector<std::string> groups = split(text, "\n\n");
  std::vector<unsigned> cals_per_elf;
  std::transform(groups.begin(), groups.end(), std::back_inserter(cals_per_elf),
                 [](const std::string &str) {
                   auto snacks = to_uint32_vec(split(str, "\n"));
                   return std::reduce(snacks.cbegin(), snacks.cend());
                 });
  std::sort(cals_per_elf.begin(), cals_per_elf.end());
  uint64_t max_cals = cals_per_elf[cals_per_elf.size() - 1];
  return max_cals;
}

/****************************************************************************************
 * @brief
 *
 * @param str:
 * @return int:
 ****************************************************************************************/
auto solve_pt2(const std::string &text) -> uint64_t {
  std::vector<std::string> groups = split(text, "\n\n");
  std::vector<unsigned> cals_per_elf;
  std::transform(groups.begin(), groups.end(), std::back_inserter(cals_per_elf),
                 [](const std::string &str) {
                   auto snacks = to_uint32_vec(split(str, "\n"));
                   return std::reduce(snacks.cbegin(), snacks.cend());
                 });
  std::sort(cals_per_elf.begin(), cals_per_elf.end());
  auto end = cals_per_elf.size() - 1;
  uint64_t max_cals =
      std::accumulate(cals_per_elf.end() - 3, cals_per_elf.end(), 0.0);
  return max_cals;
}

/****************************************************************************************
 * @brief
 *
 * @return int:
 ****************************************************************************************/
auto main() -> int {
  bool enable_example_part2 = true;
  bool enable_test_part1 = true;
  bool enable_test_part2 = true;

  if (!fs::exists(EXAMPLE_DATA_PATH)) {
    std::runtime_error("Unable to locate file: " + EXAMPLE_DATA_PATH.string());
  }
  if (!fs::exists(TEST_DATA_PATH)) {
    std::runtime_error("Unable to locate file: " + TEST_DATA_PATH.string());
  }

  std::string data1 = std::move(load(EXAMPLE_DATA_PATH));
  std::string data2{""};
  if (enable_test_part1 || enable_test_part2) {
    data2 = std::move(load(TEST_DATA_PATH));
  }

  auto example_answer1 = 24000;
  auto example_answer2 = 45000;

  auto answer1 = solve_pt1(data1);
  fmt::print("[EXAMPLE] Answer to Part 1: {}\n", answer1);
  assert(answer1 == example_answer1);

  if (enable_example_part2) {
    auto answer2 = solve_pt2(data1);
    fmt::print("[EXAMPLE] Answer to Part 2: {}\n", answer1);
    assert(answer2 == example_answer2);
  }

  if (enable_test_part1) {
    auto answer1 = solve_pt1(data2);
    fmt::print("[TEST] Answer to Part 1: {}\n", answer1);
  }

  if (enable_test_part2) {
    auto answer2 = solve_pt2(data2);
    fmt::print("[TEST] Answer to Part 2: {}\n", answer2);
  }
}
