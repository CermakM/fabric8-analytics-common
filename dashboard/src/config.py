"""Common configuration."""
import configparser
from urllib.parse import urljoin


class Config:
    """Class representing common configuration."""

    CONFIG_FILE_NAME = 'config.ini'

    def __init__(self):
        """Read and parse the configuration file."""
        self.config = configparser.ConfigParser()
        self.config.read(Config.CONFIG_FILE_NAME)

    def get_sprint(self):
        """Return name of current sprint."""
        return self.config.get('sprint', 'number')

    def get_project_url(self):
        """Return URL to a project page on GitHub."""
        try:
            url_prefix = self.config.get('issue_tracker', 'url')
            project_group = self.config.get('issue_tracker', 'group') + "/"
            project_name = self.config.get('issue_tracker', 'project_name')
            return urljoin(urljoin(url_prefix, project_group), project_name) + "/"
        except (configparser.NoSectionError, configparser.NoOptionError):
            return None

    def get_list_of_issues_url(self, team):
        """Return URL to list of issues for selected team."""
        try:
            sprint = "Sprint+" + self.config.get('sprint', 'number')
            team_label = self.config.get(team, 'label')
            project_url = self.get_project_url()
            url = '{project_url}/issues?q=is:open+is:issue+milestone:"{sprint}"+label:{label}'.\
                format(project_url=project_url, sprint=sprint, label=team_label)
            return url
        except (configparser.NoSectionError, configparser.NoOptionError):
            return None


if __name__ == "__main__":
    # execute simple checks, but only if run this module as a script
    config = Config()
    print(config.get_project_url())
    print(config.get_list_of_issues_url('core'))
    print(config.get_list_of_issues_url('integration'))
