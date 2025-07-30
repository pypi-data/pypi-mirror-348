import asyncio
import logging
from typing import (
    Dict,
    List,
    Optional
)

import httpx
from mcp.server.fastmcp import FastMCP

from qonto_mcp_server.config import (
    API_KEY,
    BASE_URL,
    STAGING_TOKEN
)

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)

logger = logging.getLogger(__name__)

async def create_supplier_invoices(
    supplier_invoices: List[Dict[str, str]],
    meta: Optional[Dict[str, str]] = None
) -> Dict:
    """
    Create supplier invoices in bulk for the authenticated organization.

    This endpoint lets you upload several supplier-invoice PDF files at once.
    Each invoice can (optionally) be protected with its own idempotency key.
    You may also provide a *meta* payload used by Qonto to power partner
    integrations (e.g. {"integration_type": "amazon", "connector": "grover"}).

    Args:
        supplier_invoices (List[Dict[str, str]]):  
            A list of objects, each containing:  
            • file_path (str, key "file_path"): local path of the PDF to upload.  
            • idempotency_key (str, optional): UUID used to safely retry a
              single-invoice upload without side-effects.
            Example:
                [
                    {
                        "file_path": "path/to/invoice1.pdf",
                        "idempotency_key": "4d5418bb-bd0d-4df4-865c-c07afab8bb48"
                    },
                    {
                        "file_path": "path/to/invoice2.pdf"
                    }
                ]
        meta (Optional[Dict[str, str]], optional): Extra key/value data
            describing the overall upload (integration_type, connector …).

    Returns:
        out(Dict): The JSON response returned by Qonto, typically an array
        of the created supplier-invoice objects. On error, returns
        {"error": "<message>"}.
    """
    import json
    import mimetypes
    import os.path

    url = f"{BASE_URL}/supplier_invoices/bulk"

    # Do NOT preset Content-Type: httpx will choose multipart automatically.
    headers = {
        "Authorization": API_KEY,
        "Content-Type": "multipart/form-data"
    }
    if STAGING_TOKEN:
        headers["X-Qonto-Staging-Token"] = STAGING_TOKEN

    # Multipart assembly ----------------------------------------------------
    files: List[tuple] = []   # holds (field_name, (filename, fileobj, mime))
    data: Dict[str, str] = {} # classic form fields (idempotency keys, meta …)
    opened_files: List[object] = []  # we close them afterwards

    try:
        for idx, invoice in enumerate(supplier_invoices):
            # ---- file ------------------------------------------------------
            if "file_path" not in invoice:
                raise ValueError("Each supplier_invoice must contain 'file_path'.")
            file_path = invoice["file_path"]
            mime_type = (
                mimetypes.guess_type(file_path)[0] or "application/pdf"
            )

            fobj = open(file_path, "rb")
            opened_files.append(fobj)  # so we can close at the end

            files.append(
                (
                    f"supplier_invoices[{idx}][file]",
                    (os.path.basename(file_path), fobj, mime_type),
                )
            )

            # ---- idempotency key -------------------------------------------
            if invoice.get("idempotency_key"):
                data[f"supplier_invoices[{idx}][idempotency_key]"] = invoice[
                    "idempotency_key"
                ]

        # ---- meta (JSON block) ---------------------------------------------
        if meta is not None:
            data["meta"] = json.dumps(meta)

        # --------------------------------------------------------------------
        async with httpx.AsyncClient() as client:
            response = await client.post(url, headers=headers, data=data, files=files)
            response.raise_for_status()
            return response.json()

    except Exception as exc:
        logger.exception("%s", exc)
        return {"error": str(exc)}

    finally:
        # always close opened file handles
        for f in opened_files:
            try:
                f.close()
            except Exception:
                pass


print(
    asyncio.run(
        create_supplier_invoices(
            supplier_invoices=[
                {
                    "file_path": "sample-invoice.pdf",
                    "idempotency_key": "4d5418bb-bd0d-4df4-865c-c07afab8bb48"
                },
            ],
            meta={
                "test": "ouioui"
            }
        )
    )
)