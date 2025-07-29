// Backend modules that interface with rust-code-analysis
//
// Each module should expose:
// - A payload struct for the request
// - A function that receives that payload and returns Result<T, String>
// The error string will be exposed to Python as a ValueError.

pub mod comment;
// pub mod function;
pub mod metrics;
// pub mod core;
