"""
Database Migration Script
Run this to upgrade your existing database with new engagement features
"""
from app import app, db
from models import Solution, Problem, Comment, UserActivity

def migrate_database():
    """Add new columns to existing database"""
    with app.app_context():
        print("🔄 Migrating database to add engagement features...")
        
        # Drop all tables and recreate (for development)
        # WARNING: This will delete existing data!
        # For production, use proper migrations (Flask-Migrate/Alembic)
        
        response = input("⚠️  This will delete existing data. Continue? (yes/no): ")
        if response.lower() != 'yes':
            print("❌ Migration cancelled.")
            return
        
        db.drop_all()
        db.create_all()
        print("✅ Database tables recreated with new structure!")
        
        # Add sample data with new features
        print("📝 Adding enhanced sample solutions...")
        
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
            description="Hash map solution with O(n) time complexity. This approach is optimal.",
            difficulty="Easy",
            time_complexity="O(n)",
            space_complexity="O(n)",
            tags="hash-map,array,two-pointers",
            execution_time_ms=45.2,
            likes=15,
            views=250,
            bookmarks=8
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
            description="Classic binary search implementation with iterative approach",
            difficulty="Easy",
            time_complexity="O(log n)",
            space_complexity="O(1)",
            tags="binary-search,divide-and-conquer,array",
            execution_time_ms=28.7,
            likes=12,
            views=180,
            bookmarks=5,
            is_featured=True
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
            description="Dynamic programming approach for Fibonacci. Optimal solution avoiding recursion overhead.",
            difficulty="Medium",
            time_complexity="O(n)",
            space_complexity="O(n)",
            tags="dynamic-programming,fibonacci,recursion",
            execution_time_ms=52.3,
            likes=20,
            views=320,
            bookmarks=12
        )
        
        sample4 = Solution(
            problem_name="Quick Sort",
            language="Python",
            code="""def quick_sort(arr):
    if len(arr) <= 1:
        return arr
    
    pivot = arr[len(arr) // 2]
    left = [x for x in arr if x < pivot]
    middle = [x for x in arr if x == pivot]
    right = [x for x in arr if x > pivot]
    
    return quick_sort(left) + middle + quick_sort(right)

# Test
arr = [3, 6, 8, 10, 1, 2, 1]
print(quick_sort(arr))""",
            author="Diana",
            description="Elegant Python implementation using list comprehensions",
            difficulty="Medium",
            time_complexity="O(n log n)",
            space_complexity="O(n)",
            tags="sorting,divide-and-conquer,recursion",
            execution_time_ms=78.5,
            likes=18,
            views=295,
            bookmarks=10,
            is_featured=True
        )
        
        db.session.add_all([sample1, sample2, sample3, sample4])
        
        # Update problems
        for problem_name in ["Two Sum", "Binary Search", "Fibonacci Sequence", "Quick Sort"]:
            problem = Problem(name=problem_name, solution_count=1)
            db.session.add(problem)
        
        # Add sample comments
        comments = [
            Comment(solution_id=1, author="Bob", content="Great solution! Very clean and efficient."),
            Comment(solution_id=1, author="Charlie", content="I used a similar approach. Hash maps are perfect for this!"),
            Comment(solution_id=2, author="Alice", content="Excellent explanation of binary search. Thanks!"),
            Comment(solution_id=3, author="Diana", content="DP is the way to go for Fibonacci. Nice work!"),
        ]
        db.session.add_all(comments)
        
        # Add sample user activity
        users = [
            UserActivity(username="Alice", solutions_submitted=1, total_views=250, total_likes=15, comments_made=1, streak_days=5),
            UserActivity(username="Bob", solutions_submitted=1, total_views=180, total_likes=12, comments_made=2, streak_days=3, badges="🥇 Top Contributor"),
            UserActivity(username="Charlie", solutions_submitted=1, total_views=320, total_likes=20, comments_made=1, streak_days=7, badges="🔥 On Fire"),
            UserActivity(username="Diana", solutions_submitted=1, total_views=295, total_likes=18, comments_made=0, streak_days=2),
        ]
        db.session.add_all(users)
        
        db.session.commit()
        print("✅ Sample data with engagement features added!")
        
        print("\n🎉 Migration complete!")
        print(f"📊 Total solutions: {Solution.query.count()}")
        print(f"💬 Total comments: {Comment.query.count()}")
        print(f"👥 Total users: {UserActivity.query.count()}")

if __name__ == '__main__':
    migrate_database()
