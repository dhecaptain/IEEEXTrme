from app import app, db
from models import Solution, Problem

def init_database():
    """Initialize the database and create tables"""
    with app.app_context():
        # Create all tables
        db.create_all()
        print("✅ Database tables created successfully!")
        
        # Add some sample data (optional)
        if Solution.query.count() == 0:
            print("📝 Adding sample solutions...")
            
            sample1 = Solution(
                problem_name="Two Sum",
                language="Python",
                code="""def two_sum(nums, target):
    seen = {}
    for i, num in enumerate(nums):
        complement = target - num
        if complement in seen:
            return [seen[complement], i]
        seen[num] = i
    return []

# Test
print(two_sum([2, 7, 11, 15], 9))  # Output: [0, 1]""",
                author="Alice",
                description="Hash map solution with O(n) time complexity"
            )
            
            sample2 = Solution(
                problem_name="Binary Search",
                language="C++",
                code="""#include <iostream>
#include <vector>
using namespace std;

int binarySearch(vector<int>& arr, int target) {
    int left = 0, right = arr.size() - 1;
    
    while (left <= right) {
        int mid = left + (right - left) / 2;
        
        if (arr[mid] == target)
            return mid;
        else if (arr[mid] < target)
            left = mid + 1;
        else
            right = mid - 1;
    }
    
    return -1;
}

int main() {
    vector<int> arr = {1, 3, 5, 7, 9, 11};
    cout << binarySearch(arr, 7) << endl;  // Output: 3
    return 0;
}""",
                author="Bob",
                description="Classic binary search implementation"
            )
            
            sample3 = Solution(
                problem_name="Fibonacci Sequence",
                language="Java",
                code="""public class Fibonacci {
    public static long fibonacci(int n) {
        if (n <= 1) return n;
        
        long[] dp = new long[n + 1];
        dp[0] = 0;
        dp[1] = 1;
        
        for (int i = 2; i <= n; i++) {
            dp[i] = dp[i - 1] + dp[i - 2];
        }
        
        return dp[n];
    }
    
    public static void main(String[] args) {
        System.out.println(fibonacci(10));  // Output: 55
    }
}""",
                author="Charlie",
                description="Dynamic programming approach for Fibonacci"
            )
            
            db.session.add_all([sample1, sample2, sample3])
            
            # Update problem counts
            for problem_name in ["Two Sum", "Binary Search", "Fibonacci Sequence"]:
                problem = Problem(name=problem_name, solution_count=1)
                db.session.add(problem)
            
            db.session.commit()
            print("✅ Sample solutions added!")
        else:
            print("ℹ️  Database already contains data")
        
        print("\n🎉 Database initialization complete!")
        print(f"📊 Total solutions: {Solution.query.count()}")

if __name__ == '__main__':
    init_database()
