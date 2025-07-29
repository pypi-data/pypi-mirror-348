# encoding: utf-8

from flask import request
import ckan.lib.helpers as h
from ckanext.multiuploadform.lib import Helper
import ckan.plugins.toolkit as toolkit
log = __import__("logging").getLogger(__name__)


class UploadController:
    def upload_resources(package_type):
        if toolkit.g.user:
            try:
                package_name = request.form["pck_id"]
                action = request.form["save"]
                if (
                    action == "go-dataset"
                ):  # Previous button: go back to the dataset metadat
                    return h.url_for(
                        "dataset.edit", id=str(package_name), _external=True
                    )

                elif (
                    action == "go-dataset-complete"
                ):  # Add resource to an active dataset
                    Helper.add_resource(
                        package_name, request, False, int(request.form["isLink"])
                    )
                    return h.url_for(
                        "dataset.read", id=str(package_name), _external=True
                    )

                else:  # Add resource to a draft dataset
                    Helper.add_resource(
                        package_name, request, True, int(request.form["isLink"])
                    )
                    if Helper.check_plugin_enabled(
                        "resource_custom_metadata"
                    ):  # if resource_custom_metadata plugin exists:
                        return h.url_for(
                            "resource_custom_metadata.index",
                            id=str(package_name),
                            _external=True,
                        )

                    elif Helper.check_plugin_enabled(
                        "organization_group"
                    ):  # if organization_group plugin exists:
                        return h.url_for(
                            "organization_group.add_ownership_view",
                            id=str(package_name),
                            _external=True,
                        )

                    elif Helper.check_plugin_enabled(
                        "media_wiki"
                    ):  # if media_wiki plugin exists
                        return h.url_for(
                            "media_wiki.machines_view",
                            id=str(package_name),
                            _external=True,
                        )

                    return h.url_for(
                        "dataset.read", id=str(package_name), _external=True
                    )
            except Exception as e:
                log.debug(f"Error {e}")
                return toolkit.abort(400, str(e))

        else:
            return toolkit.abort(
                403, "You need to authenticate before accessing this function"
            )

    def delete_uploaded_resources():
        package_name = request.form.get("pck_id")
        filenames = request.form.get("filenames")
        if toolkit.g.user:
            package = toolkit.get_action("package_show")(
                {}, {"name_or_id": package_name}
            )
            for res in package["resources"]:
                if res["name"] in filenames:
                    toolkit.get_action("resource_delete")({}, {"id": res["id"]})
            return "True"
        else:
            return toolkit.abort(
                403, "You need to authenticate before accessing this function"
            )

    def cancel_dataset_plugin_is_enabled():
        if Helper.check_plugin_enabled("cancel_dataset_creation"):
            return True
        return False

    def get_upload_limit():
        max_size = toolkit.config.get("ckan.max_resource_size")
        if not max_size:
            return "unknown"
        elif int(int(max_size) / 1000) == 0:
            return str(int(max_size) / 1000)
        return str(int(int(max_size) / 1000))
