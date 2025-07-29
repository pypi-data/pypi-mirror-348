import pytest

from rust_code_analysis_python import remove_comments

testdata = [
    # Python (.py)
    (
        "py",
        "example.py",
        """
# This is a single-line comment
def my_function():
    print("Hello, world!")# Another comment
""",
        """

def my_function():
    print("Hello, world!")
""",
    ),
    # Rust (.rs)
    (
        "rs",
        "example.rs",
        """
// This is a single-line comment
/*
* This is a multi-line comment
* in Rust.
*/
fn main() {
    println!("Hello, world!");// Another comment
}
""",
        """





fn main() {
    println!("Hello, world!");
}
""",
    ),
    # JavaScript (.js)
    (
        "js",
        "example.js",
        """
// Single-line comment
/*
* Multi-line comment
*/
function myFunction() {
  console.log("Hello, world!");// Another comment
}
""",
        """




function myFunction() {
  console.log("Hello, world!");
}
""",
    ),
    # Java (.java)
    (
        "java",
        "Example.java",
        """
// Single-line comment
/*
* Multi-line comment
*/
public class Example {
    public static void main(String[] args) {
        System.out.println("Hello, world!");// Another comment
    }
}
""",
        """




public class Example {
    public static void main(String[] args) {
        System.out.println("Hello, world!");
    }
}
""",
    ),
    # C++ (.cpp)
    (
        "cpp",
        "example.cpp",
        """
// Single-line comment
#include <iostream>

/*
* Multi-line comment
*/
int main() {
    std::cout << "Hello, world!" << std::endl;// Another comment
    return 0;
}
""",
        """

#include <iostream>




int main() {
    std::cout << "Hello, world!" << std::endl;
    return 0;
}
""",
    ),
]

testdata = list(map(lambda row: pytest.param(*row[1:], id=row[0]), testdata))


@pytest.mark.parametrize(
    "filename, code_with_comments, code_without_comments", testdata
)
def test_comments(filename, code_with_comments, code_without_comments):
    """Should remove comments from the code"""
    result = remove_comments(filename, code_with_comments)
    assert result == code_without_comments


@pytest.mark.parametrize(
    "filename, code_with_comments, code_without_comments", testdata
)
def test_missing_comments(filename, code_with_comments, code_without_comments):
    """Should return the same code if there are no comments"""
    result = remove_comments(filename, code_without_comments)
    assert result == code_without_comments


@pytest.mark.parametrize(
    "filename", ["foo.html", "foo", ""], ids=["html", "no_extension", "empty"]
)
def test_invalid_language(filename):
    """Should raise an error for filename of unsupported or no language"""
    with pytest.raises(ValueError, match=r"extension"):
        remove_comments(filename, "foo")
