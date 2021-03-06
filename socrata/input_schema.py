import json
import requests
from socrata.http import noop, post, get
from socrata.resource import Collection, Resource, ChildResourceSpec
from socrata.output_schema import OutputSchema

class InputSchema(Resource):
    """
    This represents a schema exactly as it appeared in the source
    """
    def transform(self, uri, body):
        """
        Transform this InputSchema into an Output. Returns the
        new OutputSchema. Note that this call is async - the data
        may still be transforming even though the OutputSchema is
        returned. See OutputSchema.wait_for_finish to block until
        the
        """
        return self._subresource(OutputSchema, post(
            self.path(uri),
            auth = self.auth,
            data = json.dumps(body),
        ))

    def latest_output(self, uri):
        """
        Get the latest (most recently created) OutputSchema
        which descends from this InputSchema

        Returns:
            result (bool, OutputSchema | dict): Returns an API Result; the new OutputSchema or an error response
        """
        return self._subresource(OutputSchema, get(
            self.path(uri),
            auth = self.auth,
        ))

    def get_latest_output_schema(self):
        """
        Note that this does not make an API request

        Returns:
            output_schema (OutputSchema): Returns the latest output schema
        """
        return max(self.output_schemas, key = lambda o: o.attributes['id'])

    def child_specs(self):
        return [
            ChildResourceSpec(
                self,
                'output_schemas',
                'output_schema_links',
                'output_schemas',
                OutputSchema,
                'output_schema_id'
            )
        ]
