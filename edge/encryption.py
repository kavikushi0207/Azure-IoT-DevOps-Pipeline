import tenseal as ts
import base64

def create_context():
    """Generates the CKKS encryption context and keys optimized for IoT network limits."""
    # Reduced polynomial degree (4096) produces ciphertexts under 100KB
    context = ts.context(
        ts.SCHEME_TYPE.CKKS, 
        poly_modulus_degree=4096, 
        coeff_mod_bit_sizes=[40, 20, 40]
    )
    # Scale must match the middle bit size (2^20)
    context.global_scale = 2**20
    context.generate_galois_keys()
    return context

def encrypt_float(context, value):
    """Encrypts a float, serializes it, and encodes it to Base64 for JSON transmission."""
    encrypted_vector = ts.ckks_vector(context, [value])
    serialized_bytes = encrypted_vector.serialize()
    return base64.b64encode(serialized_bytes).decode('utf-8')

# We generate the context once when the module loads
HE_CONTEXT = create_context()