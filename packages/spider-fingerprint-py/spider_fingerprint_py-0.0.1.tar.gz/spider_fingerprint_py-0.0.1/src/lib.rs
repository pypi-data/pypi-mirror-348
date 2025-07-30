use pyo3::prelude::*;
use spider_fingerprint::{
    configs::Tier,
    spoof_viewport::{Viewport, get_random_viewport},
    EmulationConfiguration, Fingerprint, emulate 
};

#[pyclass]
#[derive(Clone)]
pub struct PyViewport {
    /// Viewport screen width in pixels.
    #[pyo3(get, set)] 
    pub width: u32,
    /// Viewport screen height in pixels.
    #[pyo3(get, set)] 
    pub height: u32,
    /// Device scale factor (e.g. retina displays). `None` means no specific scaling factor.
    #[pyo3(get, set)] 
    pub device_scale_factor: Option<f64>,
    /// Whether the viewport is emulating a mobile device.
    #[pyo3(get, set)] 
    pub emulating_mobile: bool,
    /// Whether the viewport is in landscape orientation (`true`) or portrait (`false`).
    #[pyo3(get, set)] 
    pub is_landscape: bool,
    /// Whether the viewport emulation supports touch-screen interactions.
    #[pyo3(get, set)] 
    pub has_touch: bool,
}

#[pymethods]
impl PyViewport {
    #[new]
    pub fn new(width: u32, height: u32) -> Self {
        Self {
            width, height,
            device_scale_factor: None,
            emulating_mobile: false,
            is_landscape: false,
            has_touch: false,
        }
    }

    #[staticmethod]
    pub fn random() -> Self {
        let vp = get_random_viewport();
        Self {
            width: vp.width,
            height: vp.height,
            device_scale_factor: vp.device_scale_factor,
            emulating_mobile: vp.emulating_mobile,
            is_landscape: vp.is_landscape,
            has_touch: vp.has_touch,
        }
    }
}

/// The level of stealth applied in browser fingerprint emulation.
///
/// Controls how aggressively fingerprint protections are enforced during browser emulation.
/// This setting affects performance and stealth accuracy trade-offs for automated testing.
#[pyclass(eq, eq_int)]
#[derive(Debug, Clone, Copy, PartialEq)]
pub enum PyTier {
    /// Basic spoofing protections.
    Basic,
    /// Basic spoofing including console output (allows developer tools logging).
    BasicWithConsole,
    /// Basic spoofing protections, but without WebGL spoofing.
    BasicNoWebgl,
    /// Mid-level spoofing protections, better resilience against fingerprint detection.
    Mid,
    /// Highest level spoofing protections available, aggressively targeting most fingerprinting techniques.
    Full,
    #[pyo3(name = "NoSpoof")]
    /// No spoofing or protections applied; raw fingerprint visible.
    None,
}

impl From<PyTier> for Tier {
    fn from(value: PyTier) -> Self {
        match value {
            PyTier::Basic => Tier::Basic,
            PyTier::BasicWithConsole => Tier::BasicWithConsole,
            PyTier::BasicNoWebgl => Tier::BasicNoWebgl,
            PyTier::Mid => Tier::Mid,
            PyTier::Full => Tier::Full,
            PyTier::None => Tier::None,
        }
    }
}

/// Fingerprint modes available for browser emulation.
///
/// Determines whether fingerprint protections include spoofing WebGL, GPU, or no fingerprint protections.
/// This influences how aggressively bot protections and fingerprinting methods might detect the browser session.
#[pyclass(eq, eq_int)]
#[derive(Debug, Clone, Copy, PartialEq)]
pub enum PyFingerprintMode {
    /// Basic fingerprint mode, including WebGL and GPU attempts to spoof details.
    Basic,
    /// Native GPU, using real GPU-based fingerprint (for headless instances with real hardware).
    NativeGPU,
    #[pyo3(name = "NoSpoof")]
    /// No fingerprint spoofing, exposing actual browser fingerprint fully.
    None,
}

#[pyfunction(signature = (
    user_agent, 
    tier, 
    fingerprint_mode, 
    dismiss_dialogs, 
    viewport=None, 
    eval_script=None
))]
/// Generate a JavaScript emulation script based on browser fingerprint settings and viewport configurations.
///
/// This emulation script integrates various spoofing techniques (fingerprint protection, webGL spoofing, GPU emulation, etc.) based on the provided parameters.
/// It can be injected (evaluated-on-new-document) into headless browsers or regular browser automation sessions to simulate realistic browsing profiles.
///
/// # Arguments
///
/// * `user_agent` - The full browser user agent string to emulate, used for spoofing HTTP headers and navigator details.
///
/// * `tier` - The stealth level (spoofing aggressiveness) defined by [`PyTier`]. 
///
/// * `fingerprint_mode` - Mode of browser fingerprint handling defined by [`PyFingerprintMode`].
///
/// * `dismiss_dialogs` - Automatically dismiss browser dialog prompts when set to `true`.
///
/// * `viewport` - Optional viewport screen configuration ([`PyViewport`]). Defines screen size, mobile emulation, device scale, and touch emulation.
///
/// * `eval_script` - Optional custom JavaScript code to inject and run alongside the generated spoofing scripts.
///
/// # Returns
///
/// * An `Option<String>` containing the generated JavaScript emulation script. 
///   Returns `None` if no spoofing is required based on provided parameters.
pub fn generate_emulation_script(
    user_agent: &str,
    tier: PyTier,
    fingerprint_mode: PyFingerprintMode,
    dismiss_dialogs: bool,
    viewport: Option<&PyViewport>,
    eval_script: Option<&str>,
) -> PyResult<Option<String>> {
    let user_agent = if user_agent.is_empty() {
        ua_generator::ua::spoof_chrome_ua()
    } else {
      user_agent
    };

    let fingerprint = match fingerprint_mode {
        PyFingerprintMode::Basic => Fingerprint::Basic,
        PyFingerprintMode::NativeGPU => Fingerprint::NativeGPU,
        PyFingerprintMode::None => Fingerprint::None,
    };

    let mut config = EmulationConfiguration::setup_defaults(&user_agent);

    config.tier = tier.into();
    config.fingerprint = fingerprint;
    config.dismiss_dialogs = dismiss_dialogs;

    let vp = viewport.map(|vp| Viewport {
        width: vp.width,
        height: vp.height,
        device_scale_factor: vp.device_scale_factor,
        emulating_mobile: vp.emulating_mobile,
        is_landscape: vp.is_landscape,
        has_touch: vp.has_touch,
    });

    Ok(emulate(user_agent, &config, &vp, &eval_script.map(|s| Box::new(s.to_string()))))
}

#[pymodule]
fn spider_fingerprint_py(m: &Bound<'_, PyModule>) -> PyResult<()> {
    m.add_class::<PyViewport>()?;
    m.add_class::<PyTier>()?;
    m.add_class::<PyFingerprintMode>()?;
    m.add_function(wrap_pyfunction!(generate_emulation_script, m)?)?;
    Ok(())
}