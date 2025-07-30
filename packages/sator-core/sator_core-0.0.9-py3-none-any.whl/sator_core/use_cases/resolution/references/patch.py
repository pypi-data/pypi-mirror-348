from pydantic import AnyUrl

from sator_core.models.patch.references import PatchReferences
from sator_core.models.vulnerability.metadata import VulnerabilityMetadata
from sator_core.models.vulnerability.references import VulnerabilityReferences

from sator_core.models.product.locator import ProductLocator
from sator_core.models.vulnerability.locator import VulnerabilityLocator

from sator_core.ports.driven.gateways.oss import OSSGatewayPort
from sator_core.ports.driven.persistence.storage import StoragePersistencePort
from sator_core.ports.driving.resolution.references.patch import PatchReferencesResolutionPort


class PatchReferencesResolution(PatchReferencesResolutionPort):
    def __init__(self, oss_gateway: OSSGatewayPort, storage_port: StoragePersistencePort):
        self.oss_gateway = oss_gateway
        self.storage_port = storage_port

    def search_patch_references(self, vulnerability_id: str) -> PatchReferences | None:
        vulnerability_locator = self.storage_port.load(VulnerabilityLocator, vulnerability_id)

        if vulnerability_locator:
            product_locator = self.storage_port.load(ProductLocator, vulnerability_locator.product.id)

            if product_locator:
                patch_references = self._load__from_vulnerability_references(vulnerability_id)
                patch_references = self._fetch_diff_references_from_oss(
                    vulnerability_id, product_locator, patch_references
                )

                if patch_references:
                    self.storage_port.save(patch_references, vulnerability_id)
                    return patch_references

        return None

    def _fetch_diff_references_from_oss(self, vulnerability_id: str, product_locator: ProductLocator,
                                        patch_references: PatchReferences) -> PatchReferences:
        diff_ids = []
        vulnerability_metadata = self.storage_port.load(VulnerabilityMetadata, vulnerability_id)

        if patch_references and len(patch_references.diffs) > 0:
            for diff_ref in patch_references.diffs:
                owner_id, repo_id, diff_id = self.oss_gateway.get_ids_from_url(str(diff_ref))

                if not (owner_id and repo_id and diff_id):
                    continue

                if owner_id != product_locator.product_ownership.owner_id or repo_id != product_locator.repository_id:
                    continue

                # TODO: add more checks to ensure the diff is related to the vulnerability
                diff_ids.append(diff_id)

        if not diff_ids:
            if vulnerability_metadata:
                # TODO: should include versions and fetch all commits between the reported and published date
                diff_ids = self.oss_gateway.search(
                    repo_id=product_locator.repository_id, start_date=vulnerability_metadata.reported_date,
                    end_date=vulnerability_metadata.published_date, n=10
                )

        if not patch_references:
            patch_references = PatchReferences()

        patch_references.diffs = []
        # TODO: This part should probably be moved into a separate port
        for diff_id in diff_ids:
            diff_info = self.oss_gateway.get_diff_info(product_locator.repository_id, diff_id)
            print(diff_info['date'], diff_info['message'])

            if self.oss_gateway.is_security_diff_message(diff_info['message']):
                diff_url = self.oss_gateway.get_diff_url(product_locator.repository_id, diff_id)

                if diff_url:
                    patch_references.diffs.append(AnyUrl(diff_url))

        return patch_references

    def _load__from_vulnerability_references(self, vulnerability_id: str) -> PatchReferences | None:
        vul_refs = self.storage_port.load(VulnerabilityReferences, vulnerability_id)

        if vul_refs.patches:
            patch_references = PatchReferences()

            for patch in vul_refs.patches:
                # TODO: replace this with a more robust method (through a port)
                if 'github' in patch.host:
                    patch_references.diffs.append(patch)
                elif 'openwall' in patch.host:
                    patch_references.messages.append(patch)
                else:
                    patch_references.other.append(patch)
            return patch_references

        return None
