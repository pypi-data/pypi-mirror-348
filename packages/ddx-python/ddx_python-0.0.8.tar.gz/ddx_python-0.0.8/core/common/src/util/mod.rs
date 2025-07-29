#[cfg(not(target_family = "wasm"))]
pub mod backoff;
#[cfg(not(target_family = "wasm"))]
pub mod mem;
pub mod tokenize;
#[cfg(not(target_family = "wasm"))]
pub mod tracing;

pub fn get_app_share_dir(app_name: &str) -> String {
    let mut share_dir = std::env::var("APP_SHARE").expect("APP_SHARE not set");
    share_dir.push('/');
    share_dir.push_str(app_name);
    share_dir
}
