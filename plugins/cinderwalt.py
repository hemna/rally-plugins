from rally import consts
from rally.task import scenario
from rally.plugins.openstack import scenario
from rally.plugins.openstack.scenarios.cinder import utils as cinder_utils
from rally.task import validation


@validation.add("required_services", services=[consts.Service.CINDER])
@validation.add("required_platform", platform="openstack", users=True)
@scenario.configure(context={"cleanup": ["cinder"]},
                    name="CinderWalt.create_and_delete_volumes",
                    platform="openstack")
class CreateAndDelete(cinder_utils.CinderBasic):
    def run(self, size, image=None, min_sleep=0, max_sleep=0, **kwargs):
        if image:
            kwargs["imageRef"] = image

        vol1 = self.cinder.create_volume(size, **kwargs)
        vol2 = self.cinder.create_volume(size, **kwargs)
        self.sleep_between(min_sleep, max_sleep)

        self.cinder.delete_volume(vol1)
        self.cinder.delete_volume(vol2)


@validation.add("required_services", services=[consts.Service.CINDER])
@validation.add("restricted_parameters", param_names=["name", "display_name"])
@validation.add("required_contexts", contexts=("volumes"))
@validation.add("required_platform", platform="openstack", users=True)
@scenario.configure(context={"cleanup": ["cinder"]},
                    name="CinderWalt.create_from_volume_and_delete_volume",
                    platform="openstack")
class CreateFromVolumeAndDeleteVolume(cinder_utils.CinderBasic):

    def run(self, size, min_sleep=0, max_sleep=0, **kwargs):
        """Create volume from volume and then delete it.

        Scenario for testing volume clone.Optional 'min_sleep' and 'max_sleep'
        parameters allow the scenario to simulate a pause between volume
        creation and deletion (of random duration from [min_sleep, max_sleep]).

        :param size: volume size (in GB), or
                     dictionary, must contain two values:
                         min - minimum size volumes will be created as;
                         max - maximum size volumes will be created as.
                     Should be equal or bigger source volume size

        :param min_sleep: minimum sleep time between volume creation and
                          deletion (in seconds)
        :param max_sleep: maximum sleep time between volume creation and
                          deletion (in seconds)
        :param kwargs: optional args to create a volume
        """
        source_vol = self.cinder.create_volume(size, **kwargs)
        self.sleep_between(min_sleep, max_sleep)
        volume = self.cinder.create_volume(size, source_volid=source_vol["id"],
                                           **kwargs)
        self.sleep_between(min_sleep, max_sleep)
        self.cinder.delete_volume(volume)
        self.sleep_between(min_sleep, max_sleep)
        self.cinder.delete_volume(source_vol)
