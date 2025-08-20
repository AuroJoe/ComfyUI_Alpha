import node_helpers
import comfy.utils
<<<<<<< HEAD

PREFERRED_QWENIMAGE_RESOLUTIONS = [
    (672, 1568),
    (688, 1504),
    (720, 1456),
    (752, 1392),
    (800, 1328),
    (832, 1248),
    (880, 1184),
    (944, 1104),
    (1024, 1024),
    (1104, 944),
    (1184, 880),
    (1248, 832),
    (1328, 800),
    (1392, 752),
    (1456, 720),
    (1504, 688),
    (1568, 672),
]
=======
import math
>>>>>>> upstream/master


class TextEncodeQwenImageEdit:
    @classmethod
    def INPUT_TYPES(s):
        return {"required": {
            "clip": ("CLIP", ),
            "prompt": ("STRING", {"multiline": True, "dynamicPrompts": True}),
            },
            "optional": {"vae": ("VAE", ),
                         "image": ("IMAGE", ),}}

    RETURN_TYPES = ("CONDITIONING",)
    FUNCTION = "encode"

    CATEGORY = "advanced/conditioning"

    def encode(self, clip, prompt, vae=None, image=None):
        ref_latent = None
        if image is None:
            images = []
        else:
<<<<<<< HEAD
            images = [image]
            if vae is not None:
                width = image.shape[2]
                height = image.shape[1]
                aspect_ratio = width / height
                _, width, height = min((abs(aspect_ratio - w / h), w, h) for w, h in PREFERRED_QWENIMAGE_RESOLUTIONS)
                image = comfy.utils.common_upscale(image.movedim(-1, 1), width, height, "lanczos", "center").movedim(1, -1)
=======
            samples = image.movedim(-1, 1)
            total = int(1024 * 1024)

            scale_by = math.sqrt(total / (samples.shape[3] * samples.shape[2]))
            width = round(samples.shape[3] * scale_by)
            height = round(samples.shape[2] * scale_by)

            s = comfy.utils.common_upscale(samples, width, height, "area", "disabled")
            image = s.movedim(1, -1)
            images = [image[:, :, :, :3]]
            if vae is not None:
>>>>>>> upstream/master
                ref_latent = vae.encode(image[:, :, :, :3])

        tokens = clip.tokenize(prompt, images=images)
        conditioning = clip.encode_from_tokens_scheduled(tokens)
        if ref_latent is not None:
            conditioning = node_helpers.conditioning_set_values(conditioning, {"reference_latents": [ref_latent]}, append=True)
        return (conditioning, )


NODE_CLASS_MAPPINGS = {
    "TextEncodeQwenImageEdit": TextEncodeQwenImageEdit,
}
